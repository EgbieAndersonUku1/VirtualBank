import { formatUKMobileNumber, sanitizeText, toTitle, checkIfHTMLElement, toggleSpinner, showSpinnerFor } from "./utils.js"
import { parseFormData, populateForm, profileCache } from "./formUtils.js";
import { isValidEmail } from "./emailValidator.js";
import { notificationManager } from "./notificationManager.js";
import { logError } from "./logger.js";
import { config } from "./config.js";
import fetchData from './fetch.js'
import { AlertUtils } from "./alerts.js";
import { compareTwoObjects } from "./utils.js";
import { handleAppVersionUpdate } from "./utils.js";

const accountNameElement = document.getElementById("account-name");
const accountSurnameElement = document.getElementById("account-surname");
const accountEmailElement = document.getElementById("account-email");
const accountMobileElement = document.getElementById("account-mobile");
const accountLocationElement = document.getElementById("account-location");
const accountStateElement = document.getElementById("account-state");
const accountPostcodeElement = document.getElementById("account-postcode")
const dashboardTitleElement = document.getElementById("dashboard-title");
const spinnerElement = document.getElementById("spinner2");
const profileFormButtonElement  = document.getElementById("profile-form-button");
const CSRF_TOKEN                = document.getElementById("profile-form").querySelector("input[type='hidden']").value;




let profileForm;

validatePageElements();


notificationManager.setKey(config.NOTIFICATION_KEY);
profileCache.setStorageKey(config.PROFILE_KEY);


/**
 * When the application is first loaded after the user logs in, this function checks whether
 * profile data already exists in localStorage.
 *
 * If it doesn't, a fetch request is made to the backend via `profileCache.getProfileData()`.
 * Assuming the user has already created a profile, the data is returned,
 * cached in localStorage, and used to update the UI.
 *
 * This approach ensures that when the user's page is refreshed, the profile data is rebuilt
 * from the cache rather than fetched again from the backend, reducing unnecessary API calls
 * to the database.
 */
document.addEventListener("DOMContentLoaded", () => {
    (async () => {
        try {
            const profileData = await profileCache.getProfileData();
            console.log(profileData);
            updateProfileSideBar(profileData);
           
            updateProfileButtonText(profileData ? true: false);
            notificationManager.renderUnReadMessagesCount();
         
        } catch (error) {
            console.warn("❌ Error loading profile data:", error);
        }
    })();
});

document.addEventListener("DOMContentLoaded", () => {
    handleAppVersionUpdate();
    profileForm = document.getElementById("profile-form");
    if (profileForm) {
        console.log("EventListener listening on profile form...");
        profileForm.addEventListener("submit", handleProfileForm);
    } else {
        console.warn("⚠️ Could not find profile form");
    }

});



export function handleMobileUserInputField(e) {

    const MOBILE_NUMBER_INPUT_ID = "mobile";

    if (e.target.id !== MOBILE_NUMBER_INPUT_ID) {
        return;
    }

    const santizeMobileNumber = sanitizeText(e.target.value, true);

    try {
        if (santizeMobileNumber) {
            e.target.setCustomValidity("");
            const formattedNumber = formatUKMobileNumber(santizeMobileNumber);
            e.target.value = formattedNumber;
            accountMobileElement.textContent = formattedNumber;
            return;
        }
    } catch (error) {
        e.target.setCustomValidity(error.message);
        e.target.reportValidity();
        console.warn(error);
    }

    e.target.value = santizeMobileNumber;

}


export function handleUserFirstNameInputField(e) {
    const NAME_INPUT_ID = "first-name";

    if (e.target.id !== NAME_INPUT_ID) {
        return;
    }

    const sanitizedText = sanitizeText(e.target.value, false, true, ["-"]); // allow for doubled barren names with hypens e.g John-Smith
    accountNameElement.textContent = toTitle(sanitizedText);
    e.target.value = sanitizedText;

    handleDashboardTitle(accountNameElement.textContent, accountSurnameElement.textContent);
}


export function handleUserSurnameInputField(e) {

    const SURNAME_INPUT_ID = "surname";

    if (e.target.id !== SURNAME_INPUT_ID) {
        return;
    }

    const sanitizedText = sanitizeText(e.target.value, false, true);
    accountSurnameElement.textContent = toTitle(sanitizedText);
    e.target.value = sanitizedText;
    handleDashboardTitle(accountNameElement.textContent, accountSurnameElement.textContent);
}


export function handleUserEmailInputField(e) {

    const EMAIL_INPUT_ID = "email";

    if (e.target.id !== EMAIL_INPUT_ID) {
        return;
    }
    const includeChars = ["@", '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'];
    const sanitizedEmail = sanitizeText(e.target.value, false, true, includeChars);

    e.target.value = sanitizedEmail;

    try {
        e.target.setCustomValidity("");
        isValidEmail(sanitizedEmail)
        accountEmailElement.textContent = sanitizedEmail;
    } catch (error) {
        e.target.setCustomValidity(error.message);
        e.target.reportValidity();
        console.warn(error);
    }


}


export function handleUserLocationInputField(e) {
    handleInputField({ e: e, id: "country", element: accountLocationElement, capitalize: true });
}


export function handleUserStateInputField(e) {
    handleInputField({ e: e, id: "state", element: accountStateElement, capitalize: true });
}


export function handleUserPostCodeInputField(e) {
    const includeChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'];
    handleInputField({ e: e, id: "postcode", element: accountPostcodeElement, capitalize: true, inclueChars: includeChars });
}


export function handleDashboardTitle(firstName = '', surname = '') {

    dashboardTitleElement.textContent = '';

    if (!firstName === '' || !surname === '') {

        console.warn("No first name or surname specified for dashboard")
        return;
    }

    const name = getFullName(firstName, surname);
    dashboardTitleElement.textContent = `Welcome ${toTitle(name)}`;


}


function handleInputField({ e, id, element, capitalize = false, onlyChars = true, inclueChars = [" "] }) {

    if (e.target.id !== id) {
        return;
    }

    let text;

    try {
        text = onlyChars ? sanitizeText(e.target.value, false, true, inclueChars) : e.target.value;

    } catch (error) {
        text = onlyChars ? sanitizeText(e.target.value, false, true, []) : e.target.value; // if errror is throw use  []
    }


    e.target.value = onlyChars ? text : e.target.value;
    element.textContent = capitalize ? toTitle(text) : text.toLowerCase();
}



function getFullName(firstName = '', surname = '') {
    if (typeof firstName !== "string" || typeof surname !== "string") {
        throw new Error(`The names must be string. Expected string but got ${firstName} ${surname}`);
    }
    return `${toTitle(firstName)} ${toTitle(surname)}`;
}




/**
 * Handles the profile form submission by determining whether the user 
 * intends to edit or save their profile and routes the request to the 
 * appropriate backend API accordingly.
 * 
 * Assuming the form function is valid, it reads the button label  to determine the action:
 * - 'Edit Profile' triggers a call to `handleProfileData(true)`
 * - 'Save Changes' triggers a call to `handleProfileData()`
 * 
 * @param {*} e - The event object from the form submission
 * @returns {void}
 */
async function handleProfileForm(e) {

    e.preventDefault();
  

    if (!profileForm.reportValidity()) {
        return;
    }



    const EDIT_BUTTON_NAME = 'Edit Profile';
    const SAVE_BUTTON_NAME = 'Save Changes';


    const BUTTON_NAME = document.getElementById("profile-form-button").textContent.trim();
    console.log(BUTTON_NAME)

    switch (BUTTON_NAME) {
        case EDIT_BUTTON_NAME:
            await handleProfileData(true);
            break;
        case SAVE_BUTTON_NAME:
            await handleProfileData();
            break;

    }


}




/**
 * Handles the submission of profile data by either saving new profile details 
 * or updating existing ones, depending on the `updateProfile` flag.
 * 
 * - If `updateProfile` is `false`, the function assumes this is a new profile 
 *   and sends all required fields to the `/profile/save/` endpoint.
 * - If `updateProfile` is `true`, it compares the submitted form data with the 
 *   locally cached profile and sends only the changed fields to the `/profile/update/` endpoint.
 * 
 * The function also performs form validation, alerts the user if no changes were made 
 * in update mode, and handles errors returned from the fetch operation.
 * 
 * @param {boolean} [updateProfile=false] - Indicates whether this is an update operation.
 * @returns {Promise<void>} - Resolves once the data is submitted and the response is handled.
 */
async function handleProfileData(updateProfile = false) {



    if (profileForm.checkValidity()) {

        let url = "/profile/save/";
        const formData = new FormData(profileForm);
        const requiredFields = [
            "first_name",
            "surname",
            "mobile",
            "gender",
            "maritus_status",
            "country",
            "state",
            "postcode",
            "identification_documents",
            "signature"
        ]

        let profileData = parseFormData(formData, requiredFields);
       
        if (!profileData) {
            logError("handleProfileForm", "Expected data from the profile form but got nothing");
            return;
        }

        if (updateProfile) {
            url = "/profile/update/";

            // compare the profile data extracted from the form and the latest profile data stored in the cache
            // and return only the changed data. The changed data is the data that will be sent and updated 
            // in the backend
            const cachedProfileData = await profileCache.getProfileData()
            const data              = compareTwoObjects(profileData, cachedProfileData);
            profileData             = data.changes;
         
            if (profileData === null) {
                AlertUtils.showAlert({
                    title: "No action",
                    text: "No changes were taken since the data wasn't changed",
                    icon: "info",
                    confirmButtonText: "continue",
                })

                return;
            }

        }

        let resp;
        try {
            resp = await fetchData({
                url: url,
                csrfToken: CSRF_TOKEN,
                method: "POST",
                body: profileData

            });

          

        } catch (error) {
            AlertUtils.showAlert({
                title: "Profile Information was not saved",
                text: error.message,
                icon: "error",
                confirmButtonText: "Okay",
            })
            return;
        }


        handleProfileFetchResponse(resp, resp.DATA);

    }

}


/**
 * Handles the response returned after submitting or updating the user's profile.
 * 
 * Based on the server's response, it:
 * - Displays a success alert for either profile creation or update.
 * - Adds the latest profile data to the local cache via `profileCache.addProfileData`.
 * - Compares cached data with the newly submitted data to determine if an update occurred.
 * - If there are changes, notifies the user, resets the form, and toggles the loading spinner.
 * 
 * In case of an error or a null response, appropriate alerts are shown to inform the user.
 * 
 * @param {Object|null} resp - The response object returned by the backend API.
 * @param {Object} profileData - The submitted profile data used for updating or creating the profile.
 * @returns {Promise<void>} - Resolves after processing the response and updating the UI.
 */

async function handleProfileFetchResponse(resp, profileData) {

    const TiME_IN_MS = 1000;

    if (resp !== null) {

        if (resp.SUCCESS) {
            AlertUtils.showAlert({
                title: "Profile saved",
                text: "Your profile information has been successfully updated.",
                icon: "success",
                confirmButtonText: "Okay",
            });

            updateProfileButtonText(true);
            updateFormTextButton(true);
        }

        if (resp.UPDATE) {
            AlertUtils.showAlert({
                title: "Profile updated",
                text: "Your profile information has been successfully updated.",
                icon: "success",
                confirmButtonText: "Okay",
            });
        }

        const response = await profileCache.addProfileData(profileData);

        if (response === null) {
            return;
        }

        if (response.areEqual === undefined) {
            return;
        };

        if (!response.areEqual) {

            handleProfileSaveNotification(profileForm, response.changes);
            toggleSpinner(spinnerElement, true, false);

            updateProfileButtonText(profileData);
        
            setTimeout(() => {
                profileForm.reset();
                toggleSpinner(spinnerElement, false);
            }, TiME_IN_MS);
        }

    } else if (resp && !resp.SUCCESS) {

        AlertUtils.showAlert({
            title: "Profile Information was not saved",
            text: resp.ERROR,
            icon: "error",
            confirmButtonText: "Okay",
        })
    } else {
        AlertUtils.showAlert({
            title: "Profile Information was not saved",
            text: "Error saving the profile data, please refresh or try again later",
            icon: "error",
            confirmButtonText: "Okay",
        })
    }


}




function handleProfileSaveNotification(profileFormButtonElement, data) {
    const actionType = profileFormButtonElement.textContent.trim();

    if (actionType === "Edit Profile") {
        const msg = createProfileEditMessage(data);

        if (!msg) {
            return;
        }
        notificationManager.add(msg);

    } else {
        notificationManager.add("You have successfully added your profile data to local storage");
    }


}


function createProfileEditMessage(updatedData) {

    if (updatedData === null || typeof updatedData !== "object") {
        return;
    }

    const messages = Object.entries(updatedData).map(([field, { previous, current }]) =>
        `Field <${field}> changed from <${previous}> to <${current}>. `
    );

    return messages.join("\n");


}

/**
 * Updates the profile button text based on the presence of profile data in local storage.
 */
function updateProfileButtonText(updateButton = true) {
    const profileBtn = document.getElementById("profileBtn");

    if (profileBtn) {
        profileBtn.textContent = updateButton  ? "Fetch profile information" : "Edit profile information";

    }

}

export async function handleProfileBtnClick(e) {
    const PROFilE_BTN = "profileBtn";

    if (e.target.id !== PROFilE_BTN) {
        return;
    }



    const profile = await profileCache.getProfileData();


    if (typeof profile !== "object") {
        console.warn("No profile data found");
        return;
    }


    const TiME_IN_MS = 200;
    showSpinnerFor(spinnerElement, TiME_IN_MS);
    updateProfileSideBar(profile);

    // The frontend uses camelCase keys, while Django form expects snake_case.
    // To populate the Django form correctly and ensure compatibility with the backend,
    // we map specific keys to snake_case. After populating the form,
    // we delete the original snake keys to avoid including extra fields
    // when comparing profile data later to see if the form fields has been changed
    // later (which could cause false differences).
    profile.first_name               = profile.firstName ?? '';
    profile.identification_documents = profile.identificationDocuments;
    profile.maritus_status           = profile.maritusStatus;

    delete profile.maritusStatus;
    delete profile.identificationDocuments;

    const isPopulated = populateForm(profileForm, profile);
    
    delete profile.first_name 
    
    updateFormTextButton((isPopulated && profileCache.doesCacheExist()));

}


function updateFormTextButton(updateTextButton) {
    if (updateTextButton) {
        profileFormButtonElement.textContent = "Edit Profile";
    } else {
      profileFormButtonElement.textContent = "Save Changes";   
    }
}


function updateProfileSideBar(profile) {
    if (profile === "null" || typeof profile !== "object") {
        const error = `The profile data cannot be empty and it must be an object. Expected object but got ${typeof profile} with data ${profile}`;
        logError("updatedProfile", error);
        return;
    }



    accountNameElement.textContent = toTitle(profile.firstName || '') || "Not added";
    accountSurnameElement.textContent = toTitle(profile.surname || '') || "Not added";
    accountMobileElement.textContent = profile.mobile || "Not added";
    accountLocationElement.textContent = toTitle(profile.country || '') || "Not added";
    accountPostcodeElement.textContent = profile.postcode?.toUpperCase() || "Not added";
    accountEmailElement.textContent = profile.email?.toLowerCase()
    accountStateElement.textContent = toTitle(profile.state || '') || "Not added";

}



function validatePageElements() {
    checkIfHTMLElement(accountNameElement, "The account name element");
    checkIfHTMLElement(accountSurnameElement, "The account name element");
    checkIfHTMLElement(accountEmailElement, "The account email element");
    checkIfHTMLElement(accountMobileElement, "The account mobile element");
    checkIfHTMLElement(accountLocationElement, "The account location element");
    checkIfHTMLElement(accountStateElement, "The account state element");
    checkIfHTMLElement(accountPostcodeElement, "The account postcode element");
    checkIfHTMLElement(dashboardTitleElement, "The dashboard title element");

    checkIfHTMLElement(profileFormButtonElement, "form button element");

}