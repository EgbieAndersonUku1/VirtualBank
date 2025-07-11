import { profileCache } from "./formUtils.js";


export function handleLogoutCleanup() {
    console.log("Performing cleaning up, please wait..")
    sessionStorage.removeItem("profile");
    profileCache.clearCache();
    console.log("Clean up successfully cleaned")
}