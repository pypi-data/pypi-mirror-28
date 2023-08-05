
void RegisterHstore(Oid oid);
bool IsHstore(Oid oid);
Oid GetHstoreOid();

bool IsHstoreRegistered();

PyObject* GetHstore(const char* p);
