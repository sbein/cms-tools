// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME LeptonCollectionMapDict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// The generated code does not explicitly qualifies STL entities
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "LeptonCollectionMap.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void *new_LeptonCollection(void *p = 0);
   static void *newArray_LeptonCollection(Long_t size, void *p);
   static void delete_LeptonCollection(void *p);
   static void deleteArray_LeptonCollection(void *p);
   static void destruct_LeptonCollection(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LeptonCollection*)
   {
      ::LeptonCollection *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LeptonCollection >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LeptonCollection", ::LeptonCollection::Class_Version(), "LeptonCollectionMap.h", 8,
                  typeid(::LeptonCollection), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LeptonCollection::Dictionary, isa_proxy, 4,
                  sizeof(::LeptonCollection) );
      instance.SetNew(&new_LeptonCollection);
      instance.SetNewArray(&newArray_LeptonCollection);
      instance.SetDelete(&delete_LeptonCollection);
      instance.SetDeleteArray(&deleteArray_LeptonCollection);
      instance.SetDestructor(&destruct_LeptonCollection);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LeptonCollection*)
   {
      return GenerateInitInstanceLocal((::LeptonCollection*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LeptonCollection*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LeptonCollectionArrayHasher(void *p = 0);
   static void *newArray_LeptonCollectionArrayHasher(Long_t size, void *p);
   static void delete_LeptonCollectionArrayHasher(void *p);
   static void deleteArray_LeptonCollectionArrayHasher(void *p);
   static void destruct_LeptonCollectionArrayHasher(void *p);
   static void streamer_LeptonCollectionArrayHasher(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LeptonCollectionArrayHasher*)
   {
      ::LeptonCollectionArrayHasher *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LeptonCollectionArrayHasher >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LeptonCollectionArrayHasher", ::LeptonCollectionArrayHasher::Class_Version(), "LeptonCollectionMap.h", 34,
                  typeid(::LeptonCollectionArrayHasher), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LeptonCollectionArrayHasher::Dictionary, isa_proxy, 16,
                  sizeof(::LeptonCollectionArrayHasher) );
      instance.SetNew(&new_LeptonCollectionArrayHasher);
      instance.SetNewArray(&newArray_LeptonCollectionArrayHasher);
      instance.SetDelete(&delete_LeptonCollectionArrayHasher);
      instance.SetDeleteArray(&deleteArray_LeptonCollectionArrayHasher);
      instance.SetDestructor(&destruct_LeptonCollectionArrayHasher);
      instance.SetStreamerFunc(&streamer_LeptonCollectionArrayHasher);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LeptonCollectionArrayHasher*)
   {
      return GenerateInitInstanceLocal((::LeptonCollectionArrayHasher*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LeptonCollectionArrayHasher*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LeptonCollectionMap(void *p = 0);
   static void *newArray_LeptonCollectionMap(Long_t size, void *p);
   static void delete_LeptonCollectionMap(void *p);
   static void deleteArray_LeptonCollectionMap(void *p);
   static void destruct_LeptonCollectionMap(void *p);
   static Long64_t merge_LeptonCollectionMap(void *obj, TCollection *coll,TFileMergeInfo *info);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LeptonCollectionMap*)
   {
      ::LeptonCollectionMap *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LeptonCollectionMap >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LeptonCollectionMap", ::LeptonCollectionMap::Class_Version(), "LeptonCollectionMap.h", 47,
                  typeid(::LeptonCollectionMap), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LeptonCollectionMap::Dictionary, isa_proxy, 4,
                  sizeof(::LeptonCollectionMap) );
      instance.SetNew(&new_LeptonCollectionMap);
      instance.SetNewArray(&newArray_LeptonCollectionMap);
      instance.SetDelete(&delete_LeptonCollectionMap);
      instance.SetDeleteArray(&deleteArray_LeptonCollectionMap);
      instance.SetDestructor(&destruct_LeptonCollectionMap);
      instance.SetMerge(&merge_LeptonCollectionMap);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LeptonCollectionMap*)
   {
      return GenerateInitInstanceLocal((::LeptonCollectionMap*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LeptonCollectionMap*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LeptonCollectionFilesMap(void *p = 0);
   static void *newArray_LeptonCollectionFilesMap(Long_t size, void *p);
   static void delete_LeptonCollectionFilesMap(void *p);
   static void deleteArray_LeptonCollectionFilesMap(void *p);
   static void destruct_LeptonCollectionFilesMap(void *p);
   static Long64_t merge_LeptonCollectionFilesMap(void *obj, TCollection *coll,TFileMergeInfo *info);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LeptonCollectionFilesMap*)
   {
      ::LeptonCollectionFilesMap *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LeptonCollectionFilesMap >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LeptonCollectionFilesMap", ::LeptonCollectionFilesMap::Class_Version(), "LeptonCollectionMap.h", 61,
                  typeid(::LeptonCollectionFilesMap), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LeptonCollectionFilesMap::Dictionary, isa_proxy, 4,
                  sizeof(::LeptonCollectionFilesMap) );
      instance.SetNew(&new_LeptonCollectionFilesMap);
      instance.SetNewArray(&newArray_LeptonCollectionFilesMap);
      instance.SetDelete(&delete_LeptonCollectionFilesMap);
      instance.SetDeleteArray(&deleteArray_LeptonCollectionFilesMap);
      instance.SetDestructor(&destruct_LeptonCollectionFilesMap);
      instance.SetMerge(&merge_LeptonCollectionFilesMap);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LeptonCollectionFilesMap*)
   {
      return GenerateInitInstanceLocal((::LeptonCollectionFilesMap*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LeptonCollectionFilesMap*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr LeptonCollection::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LeptonCollection::Class_Name()
{
   return "LeptonCollection";
}

//______________________________________________________________________________
const char *LeptonCollection::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollection*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LeptonCollection::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollection*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LeptonCollection::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollection*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LeptonCollection::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollection*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LeptonCollectionArrayHasher::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LeptonCollectionArrayHasher::Class_Name()
{
   return "LeptonCollectionArrayHasher";
}

//______________________________________________________________________________
const char *LeptonCollectionArrayHasher::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionArrayHasher*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LeptonCollectionArrayHasher::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionArrayHasher*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LeptonCollectionArrayHasher::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionArrayHasher*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LeptonCollectionArrayHasher::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionArrayHasher*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LeptonCollectionMap::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LeptonCollectionMap::Class_Name()
{
   return "LeptonCollectionMap";
}

//______________________________________________________________________________
const char *LeptonCollectionMap::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionMap*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LeptonCollectionMap::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionMap*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LeptonCollectionMap::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionMap*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LeptonCollectionMap::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionMap*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LeptonCollectionFilesMap::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LeptonCollectionFilesMap::Class_Name()
{
   return "LeptonCollectionFilesMap";
}

//______________________________________________________________________________
const char *LeptonCollectionFilesMap::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionFilesMap*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LeptonCollectionFilesMap::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionFilesMap*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LeptonCollectionFilesMap::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionFilesMap*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LeptonCollectionFilesMap::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonCollectionFilesMap*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void LeptonCollection::Streamer(TBuffer &R__b)
{
   // Stream an object of class LeptonCollection.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LeptonCollection::Class(),this);
   } else {
      R__b.WriteClassBuffer(LeptonCollection::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LeptonCollection(void *p) {
      return  p ? new(p) ::LeptonCollection : new ::LeptonCollection;
   }
   static void *newArray_LeptonCollection(Long_t nElements, void *p) {
      return p ? new(p) ::LeptonCollection[nElements] : new ::LeptonCollection[nElements];
   }
   // Wrapper around operator delete
   static void delete_LeptonCollection(void *p) {
      delete ((::LeptonCollection*)p);
   }
   static void deleteArray_LeptonCollection(void *p) {
      delete [] ((::LeptonCollection*)p);
   }
   static void destruct_LeptonCollection(void *p) {
      typedef ::LeptonCollection current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::LeptonCollection

//______________________________________________________________________________
void LeptonCollectionArrayHasher::Streamer(TBuffer &R__b)
{
   // Stream an object of class LeptonCollectionArrayHasher.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      R__b.CheckByteCount(R__s, R__c, LeptonCollectionArrayHasher::IsA());
   } else {
      R__c = R__b.WriteVersion(LeptonCollectionArrayHasher::IsA(), kTRUE);
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LeptonCollectionArrayHasher(void *p) {
      return  p ? new(p) ::LeptonCollectionArrayHasher : new ::LeptonCollectionArrayHasher;
   }
   static void *newArray_LeptonCollectionArrayHasher(Long_t nElements, void *p) {
      return p ? new(p) ::LeptonCollectionArrayHasher[nElements] : new ::LeptonCollectionArrayHasher[nElements];
   }
   // Wrapper around operator delete
   static void delete_LeptonCollectionArrayHasher(void *p) {
      delete ((::LeptonCollectionArrayHasher*)p);
   }
   static void deleteArray_LeptonCollectionArrayHasher(void *p) {
      delete [] ((::LeptonCollectionArrayHasher*)p);
   }
   static void destruct_LeptonCollectionArrayHasher(void *p) {
      typedef ::LeptonCollectionArrayHasher current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_LeptonCollectionArrayHasher(TBuffer &buf, void *obj) {
      ((::LeptonCollectionArrayHasher*)obj)->::LeptonCollectionArrayHasher::Streamer(buf);
   }
} // end of namespace ROOT for class ::LeptonCollectionArrayHasher

//______________________________________________________________________________
void LeptonCollectionMap::Streamer(TBuffer &R__b)
{
   // Stream an object of class LeptonCollectionMap.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LeptonCollectionMap::Class(),this);
   } else {
      R__b.WriteClassBuffer(LeptonCollectionMap::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LeptonCollectionMap(void *p) {
      return  p ? new(p) ::LeptonCollectionMap : new ::LeptonCollectionMap;
   }
   static void *newArray_LeptonCollectionMap(Long_t nElements, void *p) {
      return p ? new(p) ::LeptonCollectionMap[nElements] : new ::LeptonCollectionMap[nElements];
   }
   // Wrapper around operator delete
   static void delete_LeptonCollectionMap(void *p) {
      delete ((::LeptonCollectionMap*)p);
   }
   static void deleteArray_LeptonCollectionMap(void *p) {
      delete [] ((::LeptonCollectionMap*)p);
   }
   static void destruct_LeptonCollectionMap(void *p) {
      typedef ::LeptonCollectionMap current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around the merge function.
   static Long64_t  merge_LeptonCollectionMap(void *obj,TCollection *coll,TFileMergeInfo *) {
      return ((::LeptonCollectionMap*)obj)->Merge(coll);
   }
} // end of namespace ROOT for class ::LeptonCollectionMap

//______________________________________________________________________________
void LeptonCollectionFilesMap::Streamer(TBuffer &R__b)
{
   // Stream an object of class LeptonCollectionFilesMap.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LeptonCollectionFilesMap::Class(),this);
   } else {
      R__b.WriteClassBuffer(LeptonCollectionFilesMap::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LeptonCollectionFilesMap(void *p) {
      return  p ? new(p) ::LeptonCollectionFilesMap : new ::LeptonCollectionFilesMap;
   }
   static void *newArray_LeptonCollectionFilesMap(Long_t nElements, void *p) {
      return p ? new(p) ::LeptonCollectionFilesMap[nElements] : new ::LeptonCollectionFilesMap[nElements];
   }
   // Wrapper around operator delete
   static void delete_LeptonCollectionFilesMap(void *p) {
      delete ((::LeptonCollectionFilesMap*)p);
   }
   static void deleteArray_LeptonCollectionFilesMap(void *p) {
      delete [] ((::LeptonCollectionFilesMap*)p);
   }
   static void destruct_LeptonCollectionFilesMap(void *p) {
      typedef ::LeptonCollectionFilesMap current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around the merge function.
   static Long64_t  merge_LeptonCollectionFilesMap(void *obj,TCollection *coll,TFileMergeInfo *) {
      return ((::LeptonCollectionFilesMap*)obj)->Merge(coll);
   }
} // end of namespace ROOT for class ::LeptonCollectionFilesMap

namespace ROOT {
   static TClass *vectorlEintgR_Dictionary();
   static void vectorlEintgR_TClassManip(TClass*);
   static void *new_vectorlEintgR(void *p = 0);
   static void *newArray_vectorlEintgR(Long_t size, void *p);
   static void delete_vectorlEintgR(void *p);
   static void deleteArray_vectorlEintgR(void *p);
   static void destruct_vectorlEintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<int>*)
   {
      vector<int> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<int>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<int>", -2, "vector", 386,
                  typeid(vector<int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEintgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<int>) );
      instance.SetNew(&new_vectorlEintgR);
      instance.SetNewArray(&newArray_vectorlEintgR);
      instance.SetDelete(&delete_vectorlEintgR);
      instance.SetDeleteArray(&deleteArray_vectorlEintgR);
      instance.SetDestructor(&destruct_vectorlEintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<int> >()));

      ::ROOT::AddClassAlternate("vector<int>","std::vector<int, std::allocator<int> >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<int>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<int>*)0x0)->GetClass();
      vectorlEintgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEintgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int> : new vector<int>;
   }
   static void *newArray_vectorlEintgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int>[nElements] : new vector<int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEintgR(void *p) {
      delete ((vector<int>*)p);
   }
   static void deleteArray_vectorlEintgR(void *p) {
      delete [] ((vector<int>*)p);
   }
   static void destruct_vectorlEintgR(void *p) {
      typedef vector<int> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<int>

namespace ROOT {
   static TClass *vectorlEdoublegR_Dictionary();
   static void vectorlEdoublegR_TClassManip(TClass*);
   static void *new_vectorlEdoublegR(void *p = 0);
   static void *newArray_vectorlEdoublegR(Long_t size, void *p);
   static void delete_vectorlEdoublegR(void *p);
   static void deleteArray_vectorlEdoublegR(void *p);
   static void destruct_vectorlEdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<double>*)
   {
      vector<double> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<double>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<double>", -2, "vector", 386,
                  typeid(vector<double>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEdoublegR_Dictionary, isa_proxy, 0,
                  sizeof(vector<double>) );
      instance.SetNew(&new_vectorlEdoublegR);
      instance.SetNewArray(&newArray_vectorlEdoublegR);
      instance.SetDelete(&delete_vectorlEdoublegR);
      instance.SetDeleteArray(&deleteArray_vectorlEdoublegR);
      instance.SetDestructor(&destruct_vectorlEdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<double> >()));

      ::ROOT::AddClassAlternate("vector<double>","std::vector<double, std::allocator<double> >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<double>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<double>*)0x0)->GetClass();
      vectorlEdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEdoublegR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<double> : new vector<double>;
   }
   static void *newArray_vectorlEdoublegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<double>[nElements] : new vector<double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEdoublegR(void *p) {
      delete ((vector<double>*)p);
   }
   static void deleteArray_vectorlEdoublegR(void *p) {
      delete [] ((vector<double>*)p);
   }
   static void destruct_vectorlEdoublegR(void *p) {
      typedef vector<double> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<double>

namespace ROOT {
   static TClass *vectorlEboolgR_Dictionary();
   static void vectorlEboolgR_TClassManip(TClass*);
   static void *new_vectorlEboolgR(void *p = 0);
   static void *newArray_vectorlEboolgR(Long_t size, void *p);
   static void delete_vectorlEboolgR(void *p);
   static void deleteArray_vectorlEboolgR(void *p);
   static void destruct_vectorlEboolgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<bool>*)
   {
      vector<bool> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<bool>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<bool>", -2, "vector", 592,
                  typeid(vector<bool>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEboolgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<bool>) );
      instance.SetNew(&new_vectorlEboolgR);
      instance.SetNewArray(&newArray_vectorlEboolgR);
      instance.SetDelete(&delete_vectorlEboolgR);
      instance.SetDeleteArray(&deleteArray_vectorlEboolgR);
      instance.SetDestructor(&destruct_vectorlEboolgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<bool> >()));

      ::ROOT::AddClassAlternate("vector<bool>","std::vector<bool, std::allocator<bool> >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<bool>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEboolgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<bool>*)0x0)->GetClass();
      vectorlEboolgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEboolgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEboolgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<bool> : new vector<bool>;
   }
   static void *newArray_vectorlEboolgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<bool>[nElements] : new vector<bool>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEboolgR(void *p) {
      delete ((vector<bool>*)p);
   }
   static void deleteArray_vectorlEboolgR(void *p) {
      delete [] ((vector<bool>*)p);
   }
   static void destruct_vectorlEboolgR(void *p) {
      typedef vector<bool> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<bool>

namespace ROOT {
   static TClass *vectorlETLorentzVectorgR_Dictionary();
   static void vectorlETLorentzVectorgR_TClassManip(TClass*);
   static void *new_vectorlETLorentzVectorgR(void *p = 0);
   static void *newArray_vectorlETLorentzVectorgR(Long_t size, void *p);
   static void delete_vectorlETLorentzVectorgR(void *p);
   static void deleteArray_vectorlETLorentzVectorgR(void *p);
   static void destruct_vectorlETLorentzVectorgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<TLorentzVector>*)
   {
      vector<TLorentzVector> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<TLorentzVector>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<TLorentzVector>", -2, "vector", 386,
                  typeid(vector<TLorentzVector>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlETLorentzVectorgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<TLorentzVector>) );
      instance.SetNew(&new_vectorlETLorentzVectorgR);
      instance.SetNewArray(&newArray_vectorlETLorentzVectorgR);
      instance.SetDelete(&delete_vectorlETLorentzVectorgR);
      instance.SetDeleteArray(&deleteArray_vectorlETLorentzVectorgR);
      instance.SetDestructor(&destruct_vectorlETLorentzVectorgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<TLorentzVector> >()));

      ::ROOT::AddClassAlternate("vector<TLorentzVector>","std::vector<TLorentzVector, std::allocator<TLorentzVector> >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<TLorentzVector>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlETLorentzVectorgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<TLorentzVector>*)0x0)->GetClass();
      vectorlETLorentzVectorgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlETLorentzVectorgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlETLorentzVectorgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<TLorentzVector> : new vector<TLorentzVector>;
   }
   static void *newArray_vectorlETLorentzVectorgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<TLorentzVector>[nElements] : new vector<TLorentzVector>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlETLorentzVectorgR(void *p) {
      delete ((vector<TLorentzVector>*)p);
   }
   static void deleteArray_vectorlETLorentzVectorgR(void *p) {
      delete [] ((vector<TLorentzVector>*)p);
   }
   static void destruct_vectorlETLorentzVectorgR(void *p) {
      typedef vector<TLorentzVector> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<TLorentzVector>

namespace ROOT {
   static TClass *unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR_Dictionary();
   static void unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR_TClassManip(TClass*);
   static void *new_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p = 0);
   static void *newArray_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(Long_t size, void *p);
   static void delete_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p);
   static void deleteArray_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p);
   static void destruct_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>*)
   {
      unordered_map<array<long,3>,string,LeptonCollectionArrayHasher> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>));
      static ::ROOT::TGenericClassInfo 
         instance("unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>", -2, "unordered_map", 102,
                  typeid(unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR_Dictionary, isa_proxy, 0,
                  sizeof(unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>) );
      instance.SetNew(&new_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR);
      instance.SetNewArray(&newArray_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR);
      instance.SetDelete(&delete_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR);
      instance.SetDeleteArray(&deleteArray_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR);
      instance.SetDestructor(&destruct_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< unordered_map<array<long,3>,string,LeptonCollectionArrayHasher> >()));

      ::ROOT::AddClassAlternate("unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>","std::unordered_map<std::array<long, 3ul>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, LeptonCollectionArrayHasher, std::equal_to<std::array<long, 3ul> >, std::allocator<std::pair<std::array<long, 3ul> const, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>*)0x0)->GetClass();
      unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR_TClassManip(theClass);
   return theClass;
   }

   static void unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) unordered_map<array<long,3>,string,LeptonCollectionArrayHasher> : new unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>;
   }
   static void *newArray_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>[nElements] : new unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>[nElements];
   }
   // Wrapper around operator delete
   static void delete_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p) {
      delete ((unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>*)p);
   }
   static void deleteArray_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p) {
      delete [] ((unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>*)p);
   }
   static void destruct_unordered_maplEarraylElongcO3gRcOstringcOLeptonCollectionArrayHashergR(void *p) {
      typedef unordered_map<array<long,3>,string,LeptonCollectionArrayHasher> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class unordered_map<array<long,3>,string,LeptonCollectionArrayHasher>

namespace ROOT {
   static TClass *unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR_Dictionary();
   static void unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR_TClassManip(TClass*);
   static void *new_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p = 0);
   static void *newArray_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(Long_t size, void *p);
   static void delete_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p);
   static void deleteArray_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p);
   static void destruct_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>*)
   {
      unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>));
      static ::ROOT::TGenericClassInfo 
         instance("unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>", -2, "unordered_map", 102,
                  typeid(unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR_Dictionary, isa_proxy, 4,
                  sizeof(unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>) );
      instance.SetNew(&new_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR);
      instance.SetNewArray(&newArray_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR);
      instance.SetDelete(&delete_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR);
      instance.SetDeleteArray(&deleteArray_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR);
      instance.SetDestructor(&destruct_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher> >()));

      ::ROOT::AddClassAlternate("unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>","std::unordered_map<std::array<long, 3ul>, LeptonCollection, LeptonCollectionArrayHasher, std::equal_to<std::array<long, 3ul> >, std::allocator<std::pair<std::array<long, 3ul> const, LeptonCollection> > >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>*)0x0)->GetClass();
      unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR_TClassManip(theClass);
   return theClass;
   }

   static void unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher> : new unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>;
   }
   static void *newArray_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>[nElements] : new unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>[nElements];
   }
   // Wrapper around operator delete
   static void delete_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p) {
      delete ((unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>*)p);
   }
   static void deleteArray_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p) {
      delete [] ((unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>*)p);
   }
   static void destruct_unordered_maplEarraylElongcO3gRcOLeptonCollectioncOLeptonCollectionArrayHashergR(void *p) {
      typedef unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class unordered_map<array<long,3>,LeptonCollection,LeptonCollectionArrayHasher>

namespace {
  void TriggerDictionaryInitialization_LeptonCollectionMapDict_Impl() {
    static const char* headers[] = {
"LeptonCollectionMap.h",
0
    };
    static const char* includePaths[] = {
"/cvmfs/cms.cern.ch/slc7_amd64_gcc900/lcg/root/6.22.08-ljfedo/include/",
"/nfs/dust/cms/user/beinsam/NaturalSusy/CMSSW_11_3_1/src/cms-tools/lib/classes/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "LeptonCollectionMapDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
namespace std{template <typename _Tp, std::size_t _Nm> struct __attribute__((annotate("$clingAutoload$array")))  __attribute__((annotate("$clingAutoload$LeptonCollectionMap.h")))  array;
}
class __attribute__((annotate("$clingAutoload$LeptonCollectionMap.h")))  LeptonCollection;
class __attribute__((annotate("$clingAutoload$LeptonCollectionMap.h")))  LeptonCollectionArrayHasher;
namespace std{template <typename _Tp = void> struct __attribute__((annotate("$clingAutoload$bits/stl_function.h")))  __attribute__((annotate("$clingAutoload$string")))  equal_to;
}
namespace std{template <typename _T1, typename _T2> struct __attribute__((annotate("$clingAutoload$bits/stl_pair.h")))  __attribute__((annotate("$clingAutoload$string")))  pair;
}
namespace std{template <typename _Tp> class __attribute__((annotate("$clingAutoload$bits/allocator.h")))  __attribute__((annotate("$clingAutoload$string")))  allocator;
}
class __attribute__((annotate("$clingAutoload$LeptonCollectionMap.h")))  LeptonCollectionMap;
class __attribute__((annotate("$clingAutoload$LeptonCollectionMap.h")))  LeptonCollectionFilesMap;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "LeptonCollectionMapDict dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "LeptonCollectionMap.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"LeptonCollection", payloadCode, "@",
"LeptonCollectionArrayHasher", payloadCode, "@",
"LeptonCollectionFilesMap", payloadCode, "@",
"LeptonCollectionMap", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("LeptonCollectionMapDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_LeptonCollectionMapDict_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_LeptonCollectionMapDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_LeptonCollectionMapDict() {
  TriggerDictionaryInitialization_LeptonCollectionMapDict_Impl();
}
