import { handleMobileUserInputField, 
        handleUserFirstNameInputField, 
        handleUserSurnameInputField,
        handleUserEmailInputField,
        handleUserLocationInputField,
        handleUserStateInputField,
        handleUserPostCodeInputField,
        handleProfileBtnClick,
       } from "./profile.js";

import { handleProfileIconClick, 
        handleNotificationIconClick, 
        handleMarkAsReadClick,
        handleMarkAsUnreadClick,
        handleMarkAllAsReadClick,
        handleMarkAllAsUnReadClick,
        handleDeleteLinkClick,
        handleDeleteAllNotificationsBtnClick,

       } from "./notifications.js";

import { handleWalletPin, 
       handleAddNewCard, 
       handleCardRemovalClick,
        handleRemoveCardButtonClick,
        } from "./walletUI.js";

import { handleAddNewCardInputFields, 
       handleNewCardCloseIcon, 
       handleCVCInputField 
      } from "./add-new-card.js";

import { handleRemoveCardWindowCloseIcon } from "./pin.js";
import { handleFundForm, handleFundCloseDivIconClick, handleFundAmountLength } from "./fund-account.js";
import { handleTransferButtonClick, 
        handleDisableMatchingTransferOption,
        handleTransferToSelectOption,
        handleTransferCardClick,
        handleTransferAmountInputField,
        handleTransferCloseIcon,
      
} from "./transfer-funds.js";

import { handleTransferCloseButton } from "./progress.js";
import { handleSidBarCardClick,
        handleCloseCardManagerButton,
        handleSideBarDeleteCard,
        handleAddFundCardButtonClick,
        handleAddCloseButtonIconClick,
        handleTransferAmountButtonClick,
       } from "./sidebarCard.js";

import { handleTransferBlock } from "./sidebarCardBlocking.js";
import { handleAddFundToCardFormButtonClick } from "./sideBarFundCard.js";
import { handleSelectAccountTransferElement, 
        handleSelectCardElement, 
        handleTransferCardFieldsDisplay, 
        handleTransferCardWindowCloseIcon, 
        handleCardTransferInputField, 
        handleCardTransferAmountFormButtonClick 
        } from "./sideBarTransfer-funds.js";
import { handlePageRefresh } from "./showOnRefresh.js";
import { getLocalStorage, removeFromLocalStorage, setLocalStorage } from "./db.js";
import { config } from "./config.js";


// In most web browsers like Chrome or Firefox, data stored in localStorage persists 
// across sessions, which is useful. However, if the application's data schema or logic 
// changes (e.g., after an update), the cached localStorage data may become outdated or 
// incompatible. Since browsers don’t automatically clear or update localStorage on app updates, 
// stale data may remain until the user manually clears it or performs a hard refresh.
// 
// To handle this, the app stores a version number in localStorage. When the app version changes, 
// it clears relevant localStorage keys and updates the stored version number.
// This forces the app to start fresh with the latest data, preventing inconsistencies caused 
// by old cached values.
const APP_VERSION     = '3.0.1'; 
const CURRENT_VERSION = getLocalStorage('app_version');

if (CURRENT_VERSION !== APP_VERSION) {
  console.warn(`App version changed from ${CURRENT_VERSION || 'none'} to ${APP_VERSION}. Clearing localStorage.`);
  
  [config.PROFILE_KEY, config.WALLET_STORAGE_KEY, config.NOTIFICATION_KEY].forEach((key) => {
        removeFromLocalStorage(key);
  })
 
  setLocalStorage('app_version', APP_VERSION);
}



// elements
const dashboardElement = document.getElementById("virtualbank-dashboard");


// event listeners
dashboardElement.addEventListener("click", handleEventDelegation);
dashboardElement.addEventListener("focus", handleEventDelegation);
dashboardElement.addEventListener("blur",  handleEventDelegation);
dashboardElement.addEventListener("input", handleEventDelegation);


handlePageRefresh();


function handleEventDelegation(e) {
       
   handleProfileIconClick(e);
   handleNotificationIconClick(e);
   handleMarkAsReadClick(e);
   handleMarkAsUnreadClick(e);
   handleDeleteLinkClick(e);
   handleDeleteAllNotificationsBtnClick(e);
   handleMarkAllAsReadClick(e);
   handleMarkAllAsUnReadClick(e);
   handleMobileUserInputField(e);
   handleUserFirstNameInputField(e);
   handleUserSurnameInputField(e);
   handleUserEmailInputField(e);
   handleUserLocationInputField(e);
   handleUserStateInputField(e);
   handleUserPostCodeInputField(e);
   handleProfileBtnClick(e);
   handleWalletPin(e);
   handleAddNewCard(e);
   handleAddNewCardInputFields(e);
   handleNewCardCloseIcon(e);
   handleCVCInputField(e);
   handleCardRemovalClick(e);
   handleRemoveCardButtonClick(e);
   handleRemoveCardWindowCloseIcon(e);
   handleFundForm(e);
   handleFundCloseDivIconClick(e);
   handleFundAmountLength(e);
   handleTransferButtonClick(e);
   handleDisableMatchingTransferOption(e);
   handleTransferToSelectOption(e);
   handleTransferCardClick(e);
   handleTransferAmountInputField(e);
   handleTransferCloseButton(e);
   handleTransferCloseIcon(e);
   handleSidBarCardClick(e);
   handleCloseCardManagerButton(e);
   handleSideBarDeleteCard(e);
   handleTransferBlock(e);
   handleAddFundCardButtonClick(e);
   handleAddCloseButtonIconClick(e);
   handleAddFundCardButtonClick(e);
   handleAddFundToCardFormButtonClick(e);
   handleSelectAccountTransferElement(e);
   handleTransferAmountButtonClick(e);
   handleSelectCardElement(e);
   handleTransferCardFieldsDisplay(e);
   handleTransferCardWindowCloseIcon(e);
   handleCardTransferInputField(e);
   handleCardTransferAmountFormButtonClick(e);
}
