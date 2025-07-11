import { getSessionStorage, setSessionStorage } from "./db.js";
import { compareTwoObjects } from "./utils.js";
import { logError } from "./logger.js";
import fetchData from "./fetch.js";

/**
 * Parses FormData and extracts required fields, converting keys to camelCase.
 * 
 * @param {FormData} formData - The FormData object to be parsed.
 * @param {string[]} requiredFields - An array of field names that must be present in the FormData.
 * 
 * @returns {Object} An object containing the parsed data with keys converted to camelCase.
 * 
 * @throws {Error} If:
 *   - formData is not an instance of FormData.
 *   - requiredFields is not a non-empty array.
 *   - A required field is missing or its value is empty.
 * 
 * @example
 * const formData = new FormData();
 * formData.append("first_name", "Alice");
 * formData.append("email", "alice@example.com");
 * formData.append("mobile", "1234567890");
 * 
 * const requiredFields = ["first_name", "email", "mobile"];
 * const parsedData = parseFormData(formData, requiredFields);
 * console.log(parsedData); 
 * // Output: { firstName: "Alice", email: "alice@example.com", mobile: "1234567890" }
 */
export function parseFormData(formData, requiredFields = []) {

    if (!(formData instanceof FormData)) {
        throw new Error(`Expected a FormData object but got type ${typeof formData}`);
    }

    if (!Array.isArray(requiredFields)) {
        throw new Error(`The requiredFields argument must be an array, but got type: ${typeof requiredFields}`);
    }

    if (requiredFields.length === 0) {
        throw new Error(`The required Fields array is empty. Please provide at least one field name.`);
    }

    const result = {};

    for (const field of requiredFields) {
        const value = formData.get(field);
        
        if (!value) { 
            throw new Error(`Missing or empty required field: ${field}`);
        }
        
        const camelCaseField = field.toLowerCase().replace(/[-_](.)/g, (_, char) => char.toUpperCase());
        result[camelCaseField] = value;
    }

    return result;
}



/**
 * Populates an HTML form with data from a provided object.
 * 
 * This function takes an HTMLFormElement and a data object where the keys
 * match the `name` attributes of the form's input fields. The corresponding
 * values in the object are assigned as the values of those fields.
 * 
 * @param {HTMLFormElement} formElement - The form element to populate.
 * @param {Object} dataObject - An object containing form data as key-value pairs.
 *   The keys should match the `name` attributes of the form fields.
 * 
 * @throws {Error} If the provided `formElement` is not a valid HTMLFormElement.
 * 
 * @example
 * // HTML Form Example:
 * // <form id="profileForm">
 * //     <input type="text" name="first_name">
 * //     <input type="email" name="email">
 * //     <input type="tel" name="mobile">
 * // </form>
 * 
 * // JavaScript Usage Example:
 * const profileForm = document.getElementById("profileForm");
 * const formData = { 
 *     first_name: "Alice", 
 *     email: "alice@example.com", 
 *     mobile: "1234567890" 
 * };
 * 
 * populateForm(profileForm, formData);
 * 
 * // After execution, the form fields will have the following values:
 * // - first_name: "Alice"
 * // - email: "alice@example.com"
 * // - mobile: "1234567890"
 */
export function populateForm(formElement, dataObject) {
    if (!(formElement instanceof HTMLFormElement)) {
        throw new Error("Expected an HTMLFormElement.");
    }

    let populated = false;
    for (const [key, value] of Object.entries(dataObject)) {
    
        const input = formElement.querySelector(`[name="${key}"]`);
        if (input) {
           
            input.value = value;
                if (!populated) {
                    populated = true;
                }
            
          
        }
    }
    return populated;
}



export const profileCache = {
    _KEY: null,
    _CACHE_OBJECT: null,

    
    doesCacheExist() {
        return profileCache._CACHE_OBJECT.length === 0 ? false : true;
    },

    /**
     * Sets the key used for caching profile data.
     * This key is used to interact with both the in-memory cache and localStorage.
     */
    setStorageKey: (storageKey) => {  
        if (!storageKey || typeof storageKey !== "string") {
            throw new Error(`The storage key cannot be empty and must be a string. Got type: ${typeof storageKey}`);
        }
        profileCache._KEY = storageKey;
    },

    /**
     * Retrieves the cached profile data. 
     * If not in memory, attempts to fetch from localStorage.
     */
    getProfileData:  async () => {
        if (!profileCache._KEY) {
            throw new Error("The storage key is not set. Set the key before proceeding.");
        }

        if (profileCache._CACHE_OBJECT === null || profileCache._CACHE_OBJECT === undefined) {
            console.log("Fetching from localStorage...");
            const userProfile = getSessionStorage(profileCache._KEY);
            if (Array.isArray(userProfile) && userProfile.length === 0) {

                const profileData = await profileCache._fetchProfile();
                console.log(profileData)
                if (profileData) {
                    
                    setSessionStorage(profileCache._KEY, profileData.DATA);
                    profileCache._CACHE_OBJECT = profileData.DATA;
                    return profileCache._CACHE_OBJECT;
                }
                return null;
            }
            profileCache._CACHE_OBJECT = userProfile;
            return profileCache._CACHE_OBJECT

        } else {
            console.log("Fetching from in-memory cache...");
            console.log(profileCache._CACHE_OBJECT)
            return profileCache._CACHE_OBJECT;
        }

      
    },

     /**
     * Fetches the user profile from the backend via a `fetch` API. 
     */
    _fetchProfile: async () => {

        try {
            const profileData = await fetchData({
                url: "/profile/get/",
                method: "GET",
            });
            return profileData;
        } catch (error) {
            console.error("Failed to fetch profile:", error);
            throw error;
        }
    },

    /**
     * Clears the profile cache
     */
    clearCache: () => {
        profileCache._CACHE_OBJECT = null;
    },

    /**
     * Adds or updates profile data in cache and localStorage.
     * @param {Object} profileData - The profile data to cache.
     * @returns {boolean} - True if the data was updated successfully, false otherwise.
     */
     /**
     * Adds or updates profile data in cache and localStorage.
     * @param {Object} profileData - The profile data to cache.
     * @returns {boolean} - True if the data was updated successfully, false otherwise.
     */
   /**
     * Adds or updates profile data in cache and localStorage.
     * @param {Object} profileData - The profile data to cache.
     * @returns {boolean} - True if the data was updated successfully, false otherwise.
     */
    addProfileData: async (profileData) => {
        if (!profileCache._KEY) {
            throw new Error("The storage key is not set.");
        }

        if (typeof profileData !== "object" || profileData === null) {
            logError("addProfileData", "Invalid profile data. Expected a non-null object.");
            return false;
        }

        let previousData = await profileCache.getProfileData();
        previousData     = Array.isArray(previousData) ? {} : previousData;
 
        try {
            const data = compareTwoObjects(previousData, profileData);
       
            if (!data.areEqual) {
                console.log("Saving to cache and localStorage...");
                try {
                    setSessionStorage(profileCache._KEY, profileData);
                    profileCache._CACHE_OBJECT = profileData;
                    return data;
                } catch (error) {
                    const errorMsg = `Failed to save to localStorage: ${error}`;
                    logError("addProfileData", errorMsg);
                    return null;
                }
            }
        } catch (error) {
            console.log(`Error comparing data: ${error}`);
            return null;
        }
      
        return false; // No update needed if data hasn't changed
    }
};
