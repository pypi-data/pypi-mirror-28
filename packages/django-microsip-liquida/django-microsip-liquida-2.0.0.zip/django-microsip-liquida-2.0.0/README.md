django-microsip-liquida
=======================

Install or update
-------

### latest version ###
```
pip install --upgrade git+https://github.com/jesusmaherrera/django-microsip-liquida.git
```
### An specific release version ###
```
pip install git+https://github.com/jesusmaherrera/django-microsip-liquida.git@{ tag name }
```

Setup app
__________

Agregar 'django-microsip-liquida' a EXTRA_MODULES

Agregar a localsettings.py con datos requeridos

EXTRA_INFO = {
    'ruta_datos_facturacion': 'C:\sat',
    'enlace-liquida':{
        'facturar_a':{
            'cliente_nombre':'QUESERIA VICTORIA S.P.R. DE R.L.',
            'articulo_clave':'L001',
        },
        'ruta_carpeta_liquida':'c:\\Liquida\\',
        'empresas_a_ignorar':['426','338','352','431','801','452','1445','1447','1464','1420',],
    }
}


do C:\Users\Admin\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django-microsip-liquida\django-microsip-liquida\foxpro\exportar_a_microsip.prg
close data all
close databases
Pasos para facturar

1) Syncronizar
	- pais
	- estado
	- ciudad
	- impuestos
	- condicion de pago
	- clientes
	- grupos
	- lineas
	- articulos

2) iniciar aplicacion para descargar facturas 
	- descargar facturas hasta que se indique que se descargaron todas
	- certificar facturas
