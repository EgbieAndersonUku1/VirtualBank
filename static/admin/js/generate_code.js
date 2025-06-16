/*
 * This JavaScript file enables a "Generate Code" button 
 * on the admin verification page. When clicked, the button 
 * generates a random code and inserts it into the input field. 
 * Accessible to admin and superuser roles.
 */



window.addEventListener("load", handleLoad);


function handleLoad() {
    const codeInputField = document.getElementById("id_code");

    if (!codeInputField) {
        console.warn("The code input field element couldn't be located");
        return;
    }

    const generateButton = createGenerateCodeButton();
    generateButton.addEventListener("click", (e) => {handleGenerateButtonClick(e, codeInputField)});
    codeInputField.parentNode.appendChild(generateButton);

  
}


function handleGenerateButtonClick(e, codeInputField) {
  
    if (!(codeInputField instanceof HTMLElement)) {
        console.error(`CodeInputField is not an instance of HTMLElement. Expected an html element but got ${typeof codeInputField}`);
        return;
    }
    e.preventDefault()
    codeInputField.value = generateCodeWithXLength();
}


function createGenerateCodeButton() {

    const generateCodeBtn        = document.createElement("button");
    generateCodeBtn.id           = "gen-code-btn";
    generateCodeBtn.style.width  = "100%";
    generateCodeBtn.style.margin = "8px";
    generateCodeBtn.style.backgroundColor = "#28a745";
    generateCodeBtn.style.color           = "white";
    generateCodeBtn.style.paddingTop      = "0.375rem";
    generateCodeBtn.style.paddingBottom   = "0.375rem";
    generateCodeBtn.style.border          = "2px solid lavender";
    generateCodeBtn.textContent = "Generate Code";
    return generateCodeBtn;

}


/**
 * Generates a random numeric code of a specified length.
 *
 * Each digit is randomly selected between 0 and 9 (inclusive).
 * The result is returned as a string.
 *
 * @param {number} [length=9] - The desired length of the generated code. Defaults to 9 if not provided.
 * @returns {string} A string containing the randomly generated numeric code.
 *
 * @example
 * generateCodeWithXLength();      // e.g. "093748512"
 * generateCodeWithXLength(6);     // e.g. "402819"
 */
function generateCodeWithXLength(length = 9) {
    const code = [];

    for (let i = 0; i < length; i++) {
        const number = Math.floor(Math.random() * 10); // 0–9
        code.push(number.toString());
    }

    return code.join("");
}
