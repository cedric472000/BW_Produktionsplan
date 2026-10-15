/* Was die Seite von Firebase braucht – gebündelt nach vendor/firebase.js.
   Neu bauen:  cd tools/firebase && npm install && npm run bundle            */
export { initializeApp } from "firebase/app";
export {
  initializeAuth, indexedDBLocalPersistence, browserLocalPersistence, connectAuthEmulator,
  onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword,
  sendEmailVerification, sendPasswordResetEmail, signOut, reload
} from "firebase/auth";
export {
  initializeFirestore, connectFirestoreEmulator, doc, collection,
  getDoc, getDocs, setDoc, deleteDoc, onSnapshot
} from "firebase/firestore";
