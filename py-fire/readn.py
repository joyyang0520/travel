import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
#import random

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
#random = random.randint(1,15)

doc_ref = db.document("台中")
docs = collection_ref.where("","==", "50").get()
for doc in docs:
    print("文件內容：{}".format(doc.to_dict()))
