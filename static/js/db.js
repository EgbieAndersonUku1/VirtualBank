

export function setSessionStorage(key, value) {
   return setStorageHelper(key, value, sessionStorage, "Session storage: set error" );
}


export function setLocalStorage(key, value) {
   return setStorageHelper(key, value, localStorage, "Local storage: set error" );
}



export function getSessionStorage(key) {
    return getStorageHelper(key, sessionStorage, "Session storage")
}



export function getLocalStorage(key) {
    return getStorageHelper(key, localStorage, "Local storage")
}


function setStorageHelper(key, value,  storage, message) {
    try {
        storage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error(`${message}`, error);
    }
}


export function removeFromSessionStorage(key) {
  removeStorageHelper(key, sessionStorage)
}


export function removeFromLocalStorage(key) {
  removeStorageHelper(key, localStorage)
}


function removeStorageHelper(key, storage) {
   try {
     storage.removeItem(key);
  } catch (e) {
    console.warn(`Could not remove localStorage key ${key}:`, e);
  }
}

function getStorageHelper(key, storage, message) {
     try {
        const data = storage.getItem(key);
        return data ? JSON.parse(data) : [];
    } catch (error) {
        console.error(`${message}`, error);
        return [];
    }
}



