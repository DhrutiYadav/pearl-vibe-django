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
        container.appendChild(input);
    }

    const hiddenInput = fieldRow.querySelector('input[type="text"]');

    if (hiddenInput && hiddenInput.value) {
        hiddenInput.value.split(',').forEach(c => addPicker(c));
    } else {
        addPicker();
    }

    addBtn.addEventListener('click', () => addPicker());
});
