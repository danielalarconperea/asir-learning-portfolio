
drop funcion if exists fn_calcular_capacidad_endeudamiento;
DELIMITER //
-- (saldo_total*0.3) + (numero_cuentas*1000) + (transacciones_mes*50)
CREATE FUNCTION fn_calcular_capacidad_endeudamiento(id_cli INT)
RETURNS DECIMAL(10,2)
BEGIN
  DECLARE saldo_total DECIMAL(10,2);
  DECLARE numero_cuentas INT;
  DECLARE transacciones_mes INT;

  IF id_cli IS NULL THEN
    RETURN NULL;
  END IF;
  IF NOT EXISTS (SELECT * FROM cuentas where id_cliente = id_cli) THEN
  
  SELECT SUM(saldo) INTO saldo_total
  FROM cuentas
  WHERE id_cliente = id_cli;
  
  SELECT COUNT(*) INTO numero_cuentas
  FROM cuentas
  WHERE id_cliente = id_cli;
  
  SELECT COUNT(*) INTO transacciones_mes
  FROM transacciones
  WHERE id_cuenta IN (SELECT id_cuenta FROM cuentas WHERE id_cliente = id_cli)
  AND MONTH(fecha_hora) = MONTH(CURRENT_DATE());
  
  RETURN (saldo_total*0.3) + (numero_cuentas*1000) + (transacciones_mes*50);
END //
DELIMITER ;
Select fn_calcular_capacidad_endeudamiento(1) from clientes;




















  declare categoria_cliente varchar(200);
  declare nombre_completo varchar(200);
  declare total_saldo_todas_sus_cuentas decimal(10,2);
  declare numero_total_transacciones_en_el_año decimal(10,2);
  declare cantidad_promedio_por_transaccion decimal(10,2);
  declare saldo_promedio_por_cuenta decimal(10,2);

  into categoria_cliente, nombre_completo, total_saldo_todas_sus_cuentas, numero_total_transacciones_en_el_año, cantidad_promedio_por_transaccion, saldo_promedio_por_cuenta



SELECT cl.categoria AS categoria_cliente, cl.nombre || ' ' || cl.apellido AS nombre_completo
  INTO categoria_cliente, nombre_completo
  FROM clientes cl
  JOIN cuentas cu ON cl.id_cliente = cu.id_cliente
  where cu.activa = 1;

  SELECT SUM(cu.saldo) INTO total_saldo_todas_sus_cuentas
  FROM clientes cl
  JOin cuentas cu ON cu.id_cliente = cl.id_cliente
  where cu.activa = 1
  GROUP by cl.id_cliente;

  order by total_saldo_todas_sus_cuentas desc, numero_total_transacciones_en_el_año desc, cantidad_promedio_por_transaccion desc, saldo_promedio_por_cuenta desc;
