const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewImage = document.getElementById('previewImage');

    // Função para exibir a imagem em preview
    function showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.hidden = false;
        };
        reader.readAsDataURL(file);
    }

    // Evento para lidar com o arquivo selecionado
    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];
        if (file) {
            showImagePreview(file);
        }
    });

    // Evento para permitir o arrastar e soltar da imagem
    uploadArea.addEventListener('dragover', function(event) {
        event.preventDefault();
        uploadArea.style.backgroundColor = '#c0c0c0';  // Mudar cor ao arrastar
    });

    uploadArea.addEventListener('dragleave', function(event) {
        event.preventDefault();
        uploadArea.style.backgroundColor = '#d3d3d3';  // Retornar à cor original
    });

    uploadArea.addEventListener('drop', function(event) {
        event.preventDefault();
        uploadArea.style.backgroundColor = '#d3d3d3';  // Retornar à cor original
        const file = event.dataTransfer.files[0];
        if (file) {
            fileInput.files = event.dataTransfer.files;  // Atualiza o input de arquivo
            showImagePreview(file);
        }
    });