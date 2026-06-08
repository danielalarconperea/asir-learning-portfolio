
<?php
/**
 * Roca & Senda - Funciones del Tema
 */

function roca_senda_setup() {
    // Soporte para títulos dinámicos y menús
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    
    register_nav_menus(array(
        'primary' => __('Menú Principal', 'roca-senda'),
    ));
}
add_action('after_setup_theme', 'roca_senda_setup');

function roca_senda_enqueue_scripts() {
    // Cargamos el CSS principal del tema
    wp_enqueue_style('roca-senda-styles', get_stylesheet_uri());
    
    // En WordPress real, aquí encolaríamos el bundle JS compilado.
    // Para este prototipo, usamos Tailwind vía CDN.
    wp_enqueue_script('tailwind-cdn', 'https://cdn.tailwindcss.com', array(), null, false);
}
add_action('wp_enqueue_scripts', 'roca_senda_enqueue_scripts');
?>
