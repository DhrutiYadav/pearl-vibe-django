function syncHiddenInput() {
    const hiddenInput = document.querySelector('input[name="colors_input"]');
    const pickers = document.querySelectorAll('input[name="colors_picker[]"]');

    if (!hiddenInput) return;

    const colors = Array.from(pickers).map(p => p.value);
    hiddenInput.value = colors.join(',');
}

document.addEventListener('DOMContentLoaded', function () {
    const fieldRow = document.querySelector('.form-row.field-colors_input');
    if (!fieldRow) return;

    const container = document.createElement('div');
    container.style.marginTop = '8px';

    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.textContent = 'Add Color';
    addBtn.className = 'button';
    addBtn.style.marginBottom = '8px';

    fieldRow.appendChild(addBtn);
    fieldRow.appendChild(container);

    function addPicker(value = '#000000') {
        const input = document.createElement('input');
        input.type = 'color';
        input.name = 'colors_picker[]';
        input.value = value;
        input.style.marginRight = '6px';
        input.style.marginBottom = '6px';

        input.addEventListener('change', syncHiddenInput);

        container.appendChild(input);
        syncHiddenInput();
    }


    const hiddenInput = fieldRow.querySelector('input[type="text"]');

    if (hiddenInput && hiddenInput.value) {
        hiddenInput.value.split(',').forEach(c => addPicker(c));
    } else {
        addPicker();
    }

    addBtn.addEventListener('click', () => addPicker());
});

document.addEventListener('click', function (e) {
    const chip = e.target.closest('.color-chip.removable');
    if (!chip) return;

    const color = chip.dataset.color;

    // remove preview chip
    chip.remove();

    // remove matching color picker input
    const pickers = document.querySelectorAll('input[name="colors_picker[]"]');
    pickers.forEach(picker => {
        if (picker.value === color) {
            picker.remove();
        }
    });

    // sync hidden input
    syncHiddenInput();
});
