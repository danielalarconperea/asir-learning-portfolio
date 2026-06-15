"""
Tests de clasificación de riesgo de los verbos de firewall añadidos en Fase 3:
nft, firewall-cmd y ufw (este último sacado de la rama iptables).
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tools.policy_engine import classify, decide, RiskLevel


# --- nftables --------------------------------------------------------------

def test_nft_list_is_safe_read():
    assert classify("sudo nft list ruleset").level == RiskLevel.SAFE_READ
    assert classify("nft list table inet filter").level == RiskLevel.SAFE_READ


def test_nft_block_ip_is_low():
    # plantilla EXACTA de mitigation_manual.py
    assert classify("sudo nft add rule inet filter input ip saddr 1.2.3.4 drop").level == RiskLevel.LOW


def test_nft_flush_ruleset_is_critical():
    assert classify("sudo nft flush ruleset").level == RiskLevel.CRITICAL


def test_nft_delete_table_is_critical():
    assert classify("nft delete table inet filter").level == RiskLevel.CRITICAL


def test_nft_structural_changes_are_high():
    assert classify("nft flush chain inet filter input").level == RiskLevel.HIGH
    assert classify("nft delete chain inet filter input").level == RiskLevel.HIGH
    assert classify("nft add table inet filter").level == RiskLevel.HIGH
    assert classify("nft add chain inet filter input").level == RiskLevel.HIGH


def test_nft_f_file_is_high_or_more():
    assert classify("nft -f /etc/nftables.conf").level >= RiskLevel.HIGH


def test_nft_add_rule_without_ip_is_high():
    assert classify("nft add rule inet filter input tcp dport 22 accept").level == RiskLevel.HIGH


# --- firewalld -------------------------------------------------------------

def test_firewalld_reads_are_safe_read():
    for cmd in ("sudo firewall-cmd --list-all", "firewall-cmd --state",
                "firewall-cmd --get-zones", "firewall-cmd --query-masquerade"):
        assert classify(cmd).level == RiskLevel.SAFE_READ, cmd


def test_firewalld_block_ip_is_low():
    rich = "sudo firewall-cmd --add-rich-rule=\"rule family='ipv4' source address='1.2.3.4' drop\""
    assert classify(rich).level == RiskLevel.LOW
    assert classify("firewall-cmd --add-source=1.2.3.4").level == RiskLevel.LOW


def test_firewalld_panic_levels():
    assert classify("sudo firewall-cmd --panic-on").level == RiskLevel.CRITICAL
    assert classify("sudo firewall-cmd --panic-off").level == RiskLevel.HIGH


def test_firewalld_reload_and_persist_are_low():
    assert classify("firewall-cmd --reload").level == RiskLevel.LOW
    assert classify("firewall-cmd --runtime-to-permanent").level == RiskLevel.LOW


def test_firewalld_zone_changes_are_high():
    assert classify("firewall-cmd --set-default-zone=drop").level == RiskLevel.HIGH
    assert classify("firewall-cmd --add-port=22/tcp").level == RiskLevel.HIGH
    assert classify("firewall-cmd --add-service=http").level == RiskLevel.HIGH


# --- ufw -------------------------------------------------------------------

def test_ufw_reads_are_safe_read():
    assert classify("ufw status").level == RiskLevel.SAFE_READ
    assert classify("sudo ufw status verbose").level == RiskLevel.SAFE_READ
    assert classify("ufw show added").level == RiskLevel.SAFE_READ


def test_ufw_block_ip_is_low():
    assert classify("ufw deny from 1.2.3.4").level == RiskLevel.LOW
    assert classify("sudo ufw insert 1 deny from 1.2.3.4").level == RiskLevel.LOW


def test_ufw_reset_is_critical():
    assert classify("sudo ufw --force reset").level == RiskLevel.CRITICAL


def test_ufw_global_changes_are_high():
    assert classify("ufw disable").level == RiskLevel.HIGH
    assert classify("ufw enable").level == RiskLevel.HIGH
    assert classify("ufw default deny").level == RiskLevel.HIGH
    assert classify("ufw allow 22/tcp").level == RiskLevel.HIGH


# --- decisión (allow_direct) -----------------------------------------------

def test_decide_firewall():
    assert decide("nft list ruleset").allow_direct is True
    assert decide("ufw status").allow_direct is True
    assert decide("nft flush ruleset").allow_direct is False
    assert decide("firewall-cmd --panic-on").allow_direct is False


def test_unknown_firewall_subcommand_stays_low_not_denied():
    # firewall-cmd/ufw con flags no catalogados caen a LOW (no DENY).
    assert classify("firewall-cmd --some-future-flag").level == RiskLevel.LOW
    assert classify("ufw somethingnew").level == RiskLevel.LOW


# --- correcciones de la revisión adversarial (Fase 3) ----------------------

def test_firewalld_direct_passthrough_never_safe_read():
    # --direct/--passthrough inyectan iptables crudo: jamás auto-ejecutable como
    # lectura aunque lleven un flag de lectura (regresión de seguridad ALTA).
    poc = "sudo firewall-cmd --query-panic --direct --passthrough ipv4 -F"
    assert classify(poc).level == RiskLevel.CRITICAL      # -F (flush global) vía passthrough
    assert decide(poc).allow_direct is False
    assert classify("firewall-cmd --state --direct --passthrough ipv4 -P INPUT DROP").level >= RiskLevel.HIGH
    assert classify("firewall-cmd --list-all --direct --passthrough ipv4 -A INPUT -j ACCEPT").level >= RiskLevel.HIGH


def test_firewalld_passthrough_block_ip_is_low():
    # un passthrough que bloquea una IP concreta sí es LOW (delegado a iptables).
    assert classify("firewall-cmd --direct --passthrough ipv4 -A INPUT -s 1.2.3.4 -j DROP").level == RiskLevel.LOW


def test_firewalld_mutating_state_flags_are_high():
    assert classify("firewall-cmd --lockdown-on").level == RiskLevel.HIGH
    assert classify("firewall-cmd --load-zone-defaults=public").level == RiskLevel.HIGH


def test_firewalld_and_ufw_empty_action_is_high():
    # Solo modificadores vacíos (sin flag/acción real) -> HIGH, no LOW de relleno.
    assert classify("firewall-cmd --").level == RiskLevel.HIGH
    assert classify("ufw --force").level == RiskLevel.HIGH


def test_open_firewall_rules_are_not_low():
    # accept a 0.0.0.0/0 abre el firewall: no debe bajar a LOW por contener "una IP".
    assert classify("nft add rule inet filter input ip saddr 0.0.0.0/0 accept").level == RiskLevel.HIGH
    assert classify("ufw allow from 0.0.0.0/0").level == RiskLevel.HIGH
    # IP solo dentro de un comentario (no es selector) tampoco cuenta como IP concreta.
    assert classify('nft add rule inet filter input tcp dport 22 accept comment "1.2.3.4"').level == RiskLevel.HIGH
    # control: una IP concreta de origen sigue siendo LOW
    assert classify("nft add rule inet filter input ip saddr 1.2.3.4 drop").level == RiskLevel.LOW
