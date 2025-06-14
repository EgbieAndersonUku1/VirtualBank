import { sanitizeText } from "./utils.js";



const verificationElementDiv = document.getElementById("verification-grid-input");

verificationElementDiv.addEventListener("click",  handleCharVerificationInput);
verificationElementDiv.addEventListener("blur",   handleCharVerificationInput);
verificationElementDiv.addEventListener("change", handleCharVerificationInput);
verificationElementDiv.addEventListener("input",  handleCharVerificationInput)



function handleCharVerificationInput(e) {
  
    if (!e.target.classList.contains("verification-char")) {
        return;
    }


    e.target.value ? updateInputColor(e) : updateInputColor(e, "white", "white")
   
}


function updateInputColor(e, textColor="red", background="ghostwhite") {
    e.target.style.color       = textColor
    e.target.style.background  = background;
}