
export function enableSpinner(button, loadingText=null){
    if (!button){
        console.log("button degil");
        
        return;
    }
    // Save the original text of the button
    if (!button.dataset.originalText){
        button.dataset.originalText = button.innerHTML;
    }
    // Add Spinner and optional loading text
    const spinnerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" style="margin-right: 5px;"></span>`;
    console.log("spinner yaratildi");
    
    button.innerHTML = spinnerHTML + (loadingText || button.dataset.originalText);
    // Disable button
    button.disabled = true;
    console.log("spinner eklendi");
    
}

export function disableSpinner(button, newText=null){
    if (!button){
        return;
    }
    // Restore the original text or set the new text
    button.innerHTML = newText || button.dataset.originalText || button.innerHTML;
    // Enable the button
    button.disabled = false;
    console.log("spinner cikarildi");
    
}
