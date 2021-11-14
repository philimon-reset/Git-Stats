from . import storage
""" Create an instance of the storage object and reload existing data"""
Storage_Json = storage.FileStorage()
Storage_Json.reload()
