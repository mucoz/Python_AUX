
export const ModalType = {
    INFO: 'info',
    WARNING: 'warning',
    ERROR: 'error',
    SUCCESS: 'success'
};

export const ModalSize = {
    SMALL: 'sm',
    MEDIUM: 'md',
    LARGE: 'lg'
}

export const ModalBackdrop = {
    STATIC: 'static',
    NON_STATIC: 'dynamic'
}

export const ModalTheme = {
    //Background Color, Text Color, Info Logo color, Success Logo color, Warning Logo color, Error Logo color, Secondary Text color
    LIGHT: ['bg-white', 'text-dark', "DeepSkyBlue", "limegreen", "red", "darkorange", "#4e5461ff"],
    DARK: ['bg-dark', 'text-light', "DeepSkyBlue", "lawngreen", "red", "darkorange", "#9ca3af"],
    GLASS: ['bg-glass', 'text-light', "Cyan", "lawngreen", "red", "orange", "#f3f6fcff"]
}

export const ModalAnswer = {
    YES: 'yes',
    NO: 'no',
    CANCEL: 'cancel'
}

function generateModalID() {
    return 'modal-' + Math.random().toString(36).slice(2,9);
}

export function showOKModal(message, title, type = ModalType.INFO, size=ModalSize.MEDIUM, theme=ModalTheme.LIGHT, backdrop=ModalBackdrop.NON_STATIC) {
    // Renk ve başlık tipi belirle
    let logo = "";
    if (type == ModalType.INFO){
        logo = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[2]}" class="bi bi-info-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                    </svg>
                `
    }else if (type == ModalType.SUCCESS){
        logo = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[3]}" class="bi bi-check-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/>
                    </svg>
                `
    }else if (type == ModalType.ERROR){
        logo = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[4]}" class="bi bi-x-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                    </svg>
                `
    }else if (type == ModalType.WARNING){
        logo = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[5]}" class="bi bi-exclamation-triangle" viewBox="0 0 16 16">
                    <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/>
                    <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
                    </svg>
                `
    }
    
    const modalId = generateModalID();
    injectGlassModalStyles();
    const modalHTML = `
    <div class="modal fade" id="${modalId}" tabindex="-1" aria-hidden="true" data-bs-backdrop="${backdrop}">
        <div class="modal-dialog modal-dialog-centered modal-${size}">
            <div class="modal-content ${theme[0]}">
                <div class="modal-header mt-3" style="padding:0.5rem 1rem; border: none; align-items: flex-start;">
                    
                    <div class="p-3 d-flex ${theme[1]}" style="padding-bottom: 0 !important;">
                        ${logo}
                    </div>
                    
                    <div class="flex-grow-1 p-1 d-flex flex-column justify-content-between ">
                        <h5 class="modal-title fw-bold ${theme[1]}" style="font-size: 0.95rem !important;">${title}</h5>
                        
                        <div class="modal-body p-0 mt-2 mb-2"  style="color: ${theme[6]}; font-size: 0.85rem !important;">${message}</div>
                        <div class="d-flex justify-content-end mt-2 gap-2">
                            <button type="button" class="btn btn-secondary btn-${size} fw-semibold" data-bs-dismiss="modal" aria-label="Close" style="font-size: 0.85rem;">Close</button>
                            <button type="button" class="btn btn-danger btn-${size} fw-semibold" data-bs-dismiss="modal" style="font-size: 0.85rem;">Okay</button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
    `;
    const modalWrapper = document.createElement('div');
    modalWrapper.innerHTML = modalHTML;
    document.body.appendChild(modalWrapper);

    // Modal elementini seç
    const modalElement = modalWrapper.querySelector("#" + modalId);

    // Bootstrap modal nesnesi oluştur
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

    modalElement.addEventListener('hidden.bs.modal', () => {
        setTimeout(() => {
            modal.dispose();
            modalWrapper.remove();
        }, 10);
    });
}


export function showConfirmModal(message, title, type = ModalType.INFO, size=ModalSize.MEDIUM, theme=ModalTheme.LIGHT, backdrop=ModalBackdrop.NON_STATIC){
    return new Promise((resolve) => {
        
        let logo = "";
        if (type == ModalType.INFO){
            logo = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[2]}" class="bi bi-info-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/>
                        </svg>
                    `
        }else if (type == ModalType.SUCCESS){
            logo = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[3]}" class="bi bi-check-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="m10.97 4.97-.02.022-3.473 4.425-2.093-2.094a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05"/>
                        </svg>
                    `
        }else if (type == ModalType.ERROR){
            logo = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[4]}" class="bi bi-x-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                        </svg>
                    `
        }else if (type == ModalType.WARNING){
            logo = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="${theme[5]}" class="bi bi-exclamation-triangle" viewBox="0 0 16 16">
                        <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/>
                        <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
                        </svg>
                    `
        }
        
        const modalId = generateModalID();
        injectGlassModalStyles();
        const modalHTML = `
        <div class="modal fade" id="${modalId}" tabindex="-1" aria-hidden="true" data-bs-backdrop="${backdrop}">
            <div class="modal-dialog modal-dialog-centered modal-${size}">
                <div class="modal-content ${theme[0]}">
                    <div class="modal-header mt-3" style="padding:0.5rem 1rem; border: none; align-items: flex-start;">
                        
                        <div class="p-3 d-flex ${theme[1]}" style="padding-bottom: 0 !important;">
                            ${logo}
                        </div>
                        
                        <div class="flex-grow-1 p-1 d-flex flex-column justify-content-between ">
                            <h5 class="modal-title fw-bold ${theme[1]}" style="font-size: 0.95rem !important;">${title}</h5>
                            <div class="modal-body p-0 mt-2 mb-2"  style="color: ${theme[6]}; font-size: 0.85rem !important;">${message}</div>
                            <div class="d-flex justify-content-end mt-2 gap-2">
                                <button type="button" class="btn btn-secondary btn-${size} fw-semibold" data-answer="no" data-bs-dismiss="modal" style="font-size: 0.85rem;">No</button>
                                <button type="button" class="btn btn-success btn-${size} fw-semibold" data-answer="yes" data-bs-dismiss="modal" style="font-size: 0.85rem;">Yes</button>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modalElement = document.getElementById(modalId);
        const modal = new bootstrap.Modal(modalElement);

        modalElement.querySelectorAll('[data-answer]').forEach(btn => {
            btn.addEventListener('click', () => {
                const answer = btn.dataset.answer === 'yes' ? ModalAnswer.YES : ModalAnswer.NO;
                modal.hide();
                resolve(answer);
            });
        });

        modalElement.addEventListener('hidden.bs.modal', () => {
            modalElement.remove();
        });

        modalElement.addEventListener('hide.bs.modal', (e) => {
            if (!e.target.querySelector('[data-answer]').disabled) {
                if (e.relatedTarget === null) {
                    resolve(ModalAnswer.CANCEL);
                }
            }
        });

        modal.show();
    });
};

const injectGlassModalStyles = () => {
    if (document.getElementById('bg-glass')) return;
    
    const styleTag = document.createElement('style');
    styleTag.id = 'bg-glass';
    styleTag.textContent = `
            .bg-glass{
                /* From https://css.glass */
                background: rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(5px);
                -webkit-backdrop-filter: blur(5px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
    `;
    
    document.head.appendChild(styleTag);
};
