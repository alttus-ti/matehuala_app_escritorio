# Cambios para dar de alta tarjetas nuevas

Estos cambios hacen que el Arduino pueda dar de alta una tarjeta aunque todavia
no tenga datos grabados.

## 1. Agregar funcion para enviar solo el UID

Coloca esta funcion cerca de `leerNumSerie()`:

```cpp
void enviarUidTarjeta() {
  Serial.println("uid," + rfidUid);
}
```

## 2. Cambiar `prepararBufferAlta()`

Sustituye tu funcion completa `prepararBufferAlta()` por esta version:

```cpp
bool prepararBufferAlta() {
  if (!tisc.LeerINNO(1, 0, 120, data, 0x4ACB51)) {
    Serial.println("alta,buffer_vacio");

    if (!ponerDatosPorDefectoAEV2()) {
      return false;
    }

    if (!tisc.LeerINNO(1, 0, 120, data, 0x4ACB51)) {
      Serial.println("error,leer_buffer_alta");
      return false;
    }
  }

  String vigenciaActual = leerCampoTextoDesdeData(96, 107);

  if (vigenciaActual.length() == 0) {
    if (!ponerDatosPorDefectoAEV2()) {
      return false;
    }

    if (!tisc.LeerINNO(1, 0, 120, data, 0x4ACB51)) {
      Serial.println("error,leer_buffer_default");
      return false;
    }
  }
  else if (vigenciaActual.length() != 12) {
    if (!cytibusAUrban()) {
      return false;
    }

    if (!tisc.LeerINNO(1, 0, 120, data, 0x4ACB51)) {
      Serial.println("error,leer_buffer_cytibus");
      return false;
    }
  }

  return true;
}
```

## 3. Cambiar `crearAplicacionesSiNoExisten()`

Sustituye tu funcion completa `crearAplicacionesSiNoExisten()` por esta version.
En tarjetas nuevas, `SelftestAlex()` puede fallar porque no hay aplicaciones
previas que borrar; por eso ahora se toma como limpieza opcional y se intenta
crear las aplicaciones de todos modos.

```cpp
bool crearAplicacionesSiNoExisten() {
  if (verificarAplicacionesEV2()) {
    return true;
  }

  Serial.println("alta,creando_aplicaciones");

  bool realizadoBorrarApp = tisc.SelftestAlex();
  int intentosBorrar = 0;

  while ((intentosBorrar < 3) && realizadoBorrarApp == false) {
    delay(50);
    realizadoBorrarApp = tisc.SelftestAlex();
    intentosBorrar++;
  }

  if (!realizadoBorrarApp) {
    Serial.println("alta,borrado_no_necesario_o_fallido");
  }

  bool realizadoCrear = tisc.AplicacionesINNOERNP(fileOffsetLenWrite, fileOffsetLenWriteLimite);
  int intentosCrear = 0;

  while ((intentosCrear < 3) && realizadoCrear == false) {
    delay(100);
    realizadoCrear = tisc.AplicacionesINNOERNP(fileOffsetLenWrite, fileOffsetLenWriteLimite);
    intentosCrear++;
  }

  if (!realizadoCrear) {
    Serial.println("error,crear_aplicaciones");
    msg(115, 150, WHITE, 2, "ERROR");
    delay(2500);
    saludoInicial();
    return false;
  }

  delay(200);

  if (!verificarAplicacionesEV2()) {
    Serial.println("error,verificar_aplicaciones_creadas");
    msg(115, 150, WHITE, 2, "ERROR");
    delay(2500);
    saludoInicial();
    return false;
  }

  return true;
}
```

## 4. Cambiar el inicio del bloque `if (tarjetaPresente())`

Dentro de `loop()`, busca esta parte:

```cpp
if (tarjetaPresente()) {
  if (instruccion == "ok") {
```

Y dejala asi:

```cpp
if (tarjetaPresente()) {
  if (instruccion == "uid") {
    instruccion = "";
    enviarUidTarjeta();
    return;
  }

  if (instruccion == "ok") {
```

## 5. Cambiar deteccion automatica de tarjeta

Busca esta parte:

```cpp
} else if (tarjetaPresente()) {
  if (rfidUidAnterior != rfidUid) {
    verSaldo(true);
    delay(1000);
    saludoInicial();
  }
}
```

## 6. Alta con UID enviada por Python

Python debe mandar siempre este formato:

```text
al,VIGENCIA,UID,NOMBRE,CADUCIDAD,NUMERO,TIPO
```

Normalmente la UID sale de la tarjeta presente. Para eso Arduino debe responder
al comando `uid` con:

```text
uid,<UID>
```

Si Arduino no responde `uid,<UID>`, Python puede crear una UID logica, por
ejemplo `04A1B2C3D4E5F6`. En ese caso Arduino debe aceptar la UID recibida en
la trama `al,...` y no compararla contra la UID fisica `rfidUid`.

Dentro de `darDeAltaTarjeta(String instruccion)`, sustituye la parte donde
parseas `partes` por esta:

```cpp
  String partes[8];
  int total = splitCSV(instruccion, partes, 8);

  String vigenciaAPoner = "";
  String tarjetaUID = "";
  String nombreAlta = "";
  String caducidadAlta = "";
  String numeroAlta = "";
  String tipoAlta = "";

  // Formato corto con UID:
  // al,VIGENCIA,UID,NOMBRE,TIPO
  if (total == 5) {
    vigenciaAPoner = partes[1];
    tarjetaUID = partes[2];
    nombreAlta = partes[3];
    tipoAlta = partes[4];

    if (vigenciaAPoner.length() >= 6) {
      caducidadAlta = vigenciaAPoner.substring(0, 6);
    } else {
      caducidadAlta = "000000";
    }

    numeroAlta = "00000";
  }
  // Formato completo con UID:
  // al,VIGENCIA,UID,NOMBRE,CADUCIDAD,NUMERO,TIPO
  else if (total >= 7) {
    vigenciaAPoner = partes[1];
    tarjetaUID = partes[2];
    nombreAlta = partes[3];
    caducidadAlta = partes[4];
    numeroAlta = partes[5];
    tipoAlta = partes[6];
  } else {
    Serial.println("error,alta_formato");
    return false;
  }
```

Si vas a usar UID logica generada por Python, no dejes esta validacion:

```cpp
  tarjetaUID.trim();
  tarjetaUID.toUpperCase();
  tipoAlta.trim();
  tipoAlta.toUpperCase();

  if (tarjetaUID != rfidUid) {
    Serial.println("error,uid");
    msg(115, 150, WHITE, 2, "ERROR");
    delay(2500);
    saludoInicial();
    return false;
  }
```

Sustituyela por esta:

```cpp
  tarjetaUID.trim();
  tarjetaUID.toUpperCase();
  tipoAlta.trim();
  tipoAlta.toUpperCase();

  if (tarjetaUID.length() == 0) {
    Serial.println("error,uid");
    msg(115, 150, WHITE, 2, "ERROR");
    delay(2500);
    saludoInicial();
    return false;
  }
```

Y sustituyela por esta:

```cpp
} else if (tarjetaPresente()) {
  if (rfidUidAnterior != rfidUid) {
    enviarUidTarjeta();
    rfidUidAnterior = rfidUid;

    verSaldo(true);
    delay(1000);
    saludoInicial();
  }
}
```

## Flujo esperado

Python envia:

```text
uid
```

Arduino responde:

```text
uid,04A1B2C3D4E5F6
```

Python envia el alta:

```text
al,VIGENCIA,UID,NOMBRE,CADUCIDAD,NUMERO,TIPO
```

Ejemplo:

```text
al,260415235959,04A1B2C3D4E5F6,JUAN,260415,00001,NM
```
