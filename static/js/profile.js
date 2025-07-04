import { formatUKMobileNumber, sanitizeText, toTitle, checkIfHTMLElement, toggleSpinner, showSpinnerFor } from "./utils.js"
import { parseFormData, populateForm, profileCache } from "./formUtils.js";
import { isValidEmail } from "./emailValidator.js";
import { notificationManager } from "./notificationManager.js";
import { logError } from "./logger.js";
import { config } from "./config.js";
import fetchData from './fetch.js'
import { AlertUtils } from "./alerts.js";

const accountNameElement = document.getElementById("account-name");
const accountSurnameElement = document.getElementById("account-surname");
const accountEmailElement = document.getElementById("account-email");
const accountMobileElement = document.getElementById("account-mobile");
const accountLocationElement = document.getElementById("account-location");
const accountStateElement = document.getElementById("account-state");
const accountPostcodeElement = document.getElementById("account-postcode")
const dashboardTitleElement = document.getElementById("dashboard-title");
// const profileFormElement       = document.getElementById("profile-form");
const profileBtn = document.getElementById("profileBtn");
const spinnerElement = document.getElementById("spinner2");
const profileFormButtonElement = document.getElementById("profile-form-button");
const CSRF_TOKEN = document.getElementById("profile-form").querySelector("input[type='hidden']").value;



let profileForm;

validatePageElements();


notificationManager.setKey(config.NOTIFICATION_KEY);
profileCache.setStorageKey(config.PROFILE_KEY);


document.addEventListener("DOMContentLoaded", () => {

    updateProfileSideBar(profileCache.getProfileData());
    notificationManager.renderUnReadMessagesCount();
    updateProfileButtonText();

    profileForm = document.getElementById("profile-form");
    if (profileForm) {
        console.log("EventListener listening on profile form...")
        profileForm.addEventListener("submit", handleProfileForm);
    } else {
        console.warn("⚠️ Could not find profile form");
    }

})


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

    if (e.target.id != NAME_INPUT_ID) {
        return;
    }

    const sanitizedText = sanitizeText(e.target.value, false, true, ["-"]); // allow for doubled barren names with hypens e.g John-Smith
    accountNameElement.textContent = toTitle(sanitizedText);
    e.target.value = sanitizedText;

    handleDashboardTitle(accountNameElement.textContent, accountSurnameElement.textContent);
}


export function handleUserSurnameInputField(e) {

    const SURNAME_INPUT_ID = "surname";

    if (e.target.id != SURNAME_INPUT_ID) {
        return;
    }

    const sanitizedText = sanitizeText(e.target.value, false, true);
    accountSurnameElement.textContent = toTitle(sanitizedText);
    e.target.value = sanitizedText;
    handleDashboardTitle(accountNameElement.textContent, accountSurnameElement.textContent);
}


export function handleUserEmailInputField(e) {

    const EMAIL_INPUT_ID = "email";

    if (e.target.id != EMAIL_INPUT_ID) {
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

    if (e.target.id != id) {
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
    if (typeof firstName != "string" || typeof surname != "string") {
        throw new Error(`The names must be string. Expected string but got ${firstName} ${surname}`);
    }
    return `${toTitle(firstName)} ${toTitle(surname)}`;
}


// This handles the profile data
async function handleProfileForm(e) {
  
    if (!profileForm.reportValidity()) {
        return;
    }

    e.preventDefault();
   
    if (profileForm.checkValidity()) {

        const formData       = new FormData(profileForm);
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
        
            const profileData = parseFormData(formData, requiredFields);
          
            if (!profileData) {
                logError("handleProfileForm", "Expected data from the profile form but got nothing");
                return;
            }

            let resp;
            try {
                resp = await fetchData({
                    url: "/profile/save/",
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



function handleProfileFetchResponse(resp, profileData) {

    if (resp !== null && resp.SUCCESS) {
        
        AlertUtils.showAlert({
            title: "Profile Information saved",
            text: "Your profile data was successfully saved",
            icon: "success",
            confirmButtonText: "Okay",
        })

        const response = profileCache.addProfileData(profileData);

        if (response === null) {
            return;
        }

        if (response.areEqual === undefined) {
            return;
        };


        if (!response.areEqual) {

            handleProfileSaveNotification(form, response.changes);
            toggleSpinner(spinnerElement, true, false);

            updateProfileButtonText();

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

    if (updatedData === null || typeof updatedData != "object") {
        return;
    }

    const messages = Object.entries(updatedData).map(([field, { previous, current }]) =>
        `Field <${field}> changed from <${previous}> to <${current}>. `
    );

    return messages.join("\n");
    ;

}

/**
 * Updates the profile button text based on the presence of profile data in local storage.
 */
function updateProfileButtonText() {

    const profile = profileCache.getProfileData();

    if (typeof profile != "object") {
        throw new Error("Profile data must be an array.");
    }

    profileBtn.textContent = profile.length === 0
        ? "Add profile information"
        : "Edit profile information";
}


export function handleProfileBtnClick(e) {
    const PROFilE_BTN = "profileBtn";

    if (e.target.id != PROFilE_BTN) {
        return;
    }

    const profile = profileCache.getProfileData();
    if (typeof profile != "object") {
        console.warn("No profile data found");
        return;
    }

    const TiME_IN_MS = 200;

    showSpinnerFor(spinnerElement, TiME_IN_MS);
    updateProfileSideBar(profile);
    const isPopulated = populateForm(profileForm, profile);

    if (isPopulated) {
        profileFormButtonElement.textContent = "Edit Profile";
    }


}


function updateProfileSideBar(profile) {
    if (profile === "null" || typeof profile != "object") {
        const error = `The profile data cannot be empty and it must be an object. Expected object but got ${typeof profile}`;
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