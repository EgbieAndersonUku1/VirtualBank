
/**
 * Sanitizes the input text based on the specified criteria:
 * - Optionally removes non-numeric characters.
 * - Optionally removes non-alphabet characters.
 * - Optionally ensures that specific special characters are included and valid.
 * - Removes hyphens from the input text.
 *
 * @param {string} text - The input text to be sanitized.
 * @param {boolean} [onlyNumbers=false] - If true, removes all non-numeric characters.
 * @param {boolean} [onlyChars=false] - If true, removes all non-alphabetic characters.
 * @param {Array<string>} [includeChars=[]] - An array of special characters that should be included in the text.
 * @throws {Error} If `includeChars` is not an array or contains invalid characters that are not in the `specialChars` list.
 * @returns {string} - The sanitized version of the input text.
 *
 * @example
 * // Only numbers will remain (non-numeric characters removed)
 * sanitizeText('abc123', true); 
 * // Output: '123'
 *
 * @example
 * // Only alphabetic characters will remain (non-alphabet characters removed)
 * sanitizeText('abc123!@#', false, true);
 * // Output: 'abc'
 *
 * @example
 * // Ensures specific special characters are valid (will remove invalid ones)
 * sanitizeText('@hello!world', false, false, ['!', '@']);
 * // Output: '@hello!world' (if both '!' and '@' are in the valid list of special characters)
 *
 * @example
 * // Removes hyphens from the input
 * sanitizeText('my-name-is', false, false);
 * // Output: 'mynameis'
 */
export function sanitizeText(text, onlyNumbers = false, onlyChars = false, includeChars = []) {
    if (!Array.isArray(includeChars)) {
        throw new Error(`Expected an array but got type ${typeof includeChars}`);
    }

    const INCLUDE_CHARS_ARRAY_LENGTH = includeChars.length;

    if (!Array.isArray(includeChars)) {
        throw new Error(`Expected an array but got ${typeof includeChars}`);
    }

    if (INCLUDE_CHARS_ARRAY_LENGTH > 0) {
        const invalidChar = includeChars.find(char => !specialChars[char]);
        if (invalidChar) {
            throw new Error(`Expected a special character but got ${invalidChar}`);
        }
    }

    if (onlyNumbers) {
        return text.replace(/\D+/g, ""); 
    }

    if (onlyChars) {
        if (INCLUDE_CHARS_ARRAY_LENGTH > 0) {
            return text.replace(/[^A-Za-z]/g, (match) => {
                return includeChars.includes(match) ? match : '';  
            });
        }
     
        return text.replace(/[^A-Za-z]/g, '');
    }

    return text ? text.split("-").join("") : ''; 
}

