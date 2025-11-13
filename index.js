import { showOKModal, showConfirmModal, ModalType, ModalSize, ModalTheme, ModalBackdrop, ModalAnswer } from './modalUtils.js';
import { enableSpinner, disableSpinner } from './buttonUtils.js';

document.addEventListener('DOMContentLoaded', ()=>{
    const smallBtn = document.getElementById("smallBtn");
    const mediumBtn = document.getElementById("mediumBtn");
    const largeBtn = document.getElementById("largeBtn");
    smallBtn.addEventListener("click", ()=>{
        showOKModal("Are you sure you want to deactivate your account? All of your data will be permanently removed. This action cannot be undone.", "Deactivate account", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.LIGHT);
    });
    mediumBtn.addEventListener("click", ()=>{
        showOKModal("Are you sure you want to deactivate your account? All of your data will be permanently removed. This action cannot be undone.", "Deactivate account", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.DARK);
    });
    largeBtn.addEventListener("click", ()=>{
        showOKModal("Are you sure", "Deactivate account", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.GLASS, ModalBackdrop.STATIC);
    });
    const smallBtnA = document.getElementById("smallBtnA");
    const mediumBtnA = document.getElementById("mediumBtnA");
    const largeBtnA = document.getElementById("largeBtnA");
    smallBtnA.addEventListener("click", async ()=>{
        const answer = await showConfirmModal("Are you sure you want to deactivate your account? All of your data will be permanently removed. This action cannot be undone.", "Deactivate account", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.LIGHT);
        if (answer == ModalAnswer.YES){
            showOKModal("Test", "Test");
        }
    });
    mediumBtnA.addEventListener("click", ()=>{
        const answer = showConfirmModal("Are you sure you want to deactivate your account? All of your data will be permanently removed. This action cannot be undone.", "Deactivate account", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.DARK);
    });
    largeBtnA.addEventListener("click", ()=>{
        const answer = showConfirmModal("Are you sure", "Deactivate account", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.GLASS, ModalBackdrop.NON_STATIC);
    });

    
    testBtn.addEventListener("click", async () => {
        const testBtn = document.getElementById("testBtn");
        enableSpinner(testBtn, "Processing...");
        await fetch("http://127.0.0.1:5002/test_app").then((data)=>{
            console.log(data);
            throw new Error("Errorrr");
        }).catch((err)=>{
            console.log(err);  
            showOKModal(err, "Error", ModalType.ERROR, ModalSize.MEDIUM, ModalTheme.DARK, ModalBackdrop.STATIC);
        })
        disableSpinner(testBtn);
    });



})

