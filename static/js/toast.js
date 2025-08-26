function showToast(message, timer) {
    let toast = document.createElement('div');
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '32px';
    toast.style.right = '32px';
    toast.style.background = '#27ae60';
    toast.style.color = '#fff';
    toast.style.padding = '16px 28px';
    toast.style.borderRadius = '8px';
    toast.style.fontSize = '1.05rem';
    toast.style.fontWeight = '600';
    toast.style.boxShadow = '0 4px 16px rgba(39,174,96,0.18)';
    toast.style.zIndex = '9999';
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';

    document.body.appendChild(toast);

    setTimeout(() => { toast.style.opacity = '1'; }, 10);

    const destroyToast = function() {
        toast.style.opacity = '0';
        setTimeout(() => { toast.remove(); }, 300);
    };

    if (timer) {
        setTimeout(destroyToast, timer);
    } 
    return destroyToast;
}
