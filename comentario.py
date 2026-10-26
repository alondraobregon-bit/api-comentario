import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_INGESTA"]   # NUEVO
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    # 1) Grabar en DynamoDB (igual que en el Ejercicio 3)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    # 2) NUEVO - Ingesta Push: la lambda (origen) ENVIA el json al bucket S3 (destino)
    s3 = boto3.client('s3')
    nombre_archivo = tenant_id + '/' + uuidv1 + '.json'
    s3.put_object(
        Bucket=nombre_bucket,
        Key=nombre_archivo,
        Body=json.dumps(comentario, ensure_ascii=False),
        ContentType='application/json'
    )

    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'archivo_s3': 's3://' + nombre_bucket + '/' + nombre_archivo,
        'response': response
    }
