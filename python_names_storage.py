from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "coastal-stone-382223",
  "private_key_id": "2ee758f20f19b656305d32ef6ffc0a2ab6b3f073",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPyG0+3DTdxIFN\nuLso2ZGAPaCT3qYvKa1/6q1CEQQ3CUPWcdneqB4+Zkijt9/dXSQgaKdldB/7pjj+\nQ6KjbbCvFo+zJ4DvilWhZhF26DUngodnOCgalLeqfAPQLtWkiUmkdyYzoknT7oc+\ndm2WwNL5OmxJ+VQmZ9g7jHPYEUs1NQZaqKBm4iYTVIIfGM6MPNx4MCEIalD2g/cX\nJlqxdKLd8SPG4o7JzgACXaUcl9yGd9HoU6s4Gi0ackrjca34ZHquQWgXiDsR/SWU\njtN0tgGj0lFNUZYUW7/CWDdPT6uDFvUa1dn6i9ulKyk7IxvhmaRkaqU9OWUVPcfQ\ngL/hLc4hAgMBAAECgf8Ya1lCX0/XPsWhVmnkmNyp06pwrPLt5wr+hXZ1Ruypqsi8\n027Q+C0nIeezaPVbRGrExkWEG8xXcY1BK473+C6V4HLjXAOI1F2BesxmZfoFfnFC\nRMkP0ewivlDQ2s/VedTrb3QnLrXECWpaAwxTBvRigj8uTIEVsDsR7Z8xSj9Qb+ch\n8z/5ZSvVl7qWghD90SzATPW7CbtLECC7bGCNjCJkY5pGWYRyUx/yoFy6iH1+56Yy\nlaVTFW3S4UzRJXJYTV1tL3OCSyXW2evjgWDIYZ5z5NORE5nIdh9IBY4xVc4Bd639\nu8zjK9yFz4C9h4EOWJPdEWjGzVeBrSj1qk6WxSUCgYEA9h1cR22bH3RYZig3Ik3U\nj/CJ717BJiwawiBJX1+4Jaqg6602AMcrrvsfunYFOMlC9bmVVscFwe7XTzIBrpvR\nxorROjPMRiZ2eWz1WwEeaoSvO1U1nnhkCLgU3gsyXeITTSk7dlcaX+zNAYeGfXal\nIcf5unhtx0gnwVVor0t9tEMCgYEA2CDs3IF/P8823t2mbSq0aK3wFaoZT64ddOVA\nlP7CuMBZnN1B6hWgL52vdhLSOMPt4CSPjP7Hakbp+cD35C07kSevTXvO8w39T51m\n++9jo/vjyIRv8i+ONqfD2DrAJfYz0YbTUCxZx2+8KihBWoONATIaPiIQdyTAGQUJ\ngXLJX8sCgYEA9e5A199esv+/ldV5wn2jenISY2978nkABBvfNb6gdIMcamSbIgvk\nSuYFvn1Qmn4CuyjHYf9ecXwJCsodhC2QYaU1jcNUzISCvrNyOY3UpvwPXmq3ObNz\nwoKv13G40remMeSR1p8Ta+dks7KJYbW9LRR3Jy5QBGLF1xtRkFkPM6ECgYEAzrXG\n9Sth4ky0pTmHSJf0jr31hzL2HHBiOgBd4WM8J+nIi7BOr61ZVNFTFPHxYFt8csll\nBqxTXAFRHQ+DyBe/BhjXoJsOlwbFRNU9vy35tchf1tNcIl17fii8tl2Sk3xDmV2D\nVAXnJEloxUVVJFX3kbIyyURZTSq4E/XuXoHDujsCgYEAyhcq8FejdpExjJNZAMpu\nMBFlYQH+mVOtAFEjN2JV03sRbsAFtNF6l5u64n9t5OyPPz8PsJHTDrq3kU2aW3Tw\nCJJTTnTc9Zvo8V77k8cjOryZXFFLPxGrl0hDf616pl6UzmdKu2tqqreli1lMLmeO\njRz1UyUKm5zf4KuV5/7xHBs=\n-----END PRIVATE KEY-----\n",
  "client_email": "70457987015-compute@developer.gserviceaccount.com",
  "client_id": "111813469010084702239",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/70457987015-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names_lu') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
