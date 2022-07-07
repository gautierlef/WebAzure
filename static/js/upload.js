Dropzone.autoDiscover = false;

var dropzoneThread = new Dropzone("#dropzoneThread", {
    dictDefaultMessage: "Upload or drop your pictures here ! ",
    acceptedFiles: ".jpeg,.jpg,.png,.gif,.jfif",
    maxFiles: 10,
    previewsContainer: "#dropzoneArea",
    clickable: "#dropzoneArea",
    dictRemoveFile: "Remove",
    autoProcessQueue: false,
    uploadMultiple: true,
    parallelUploads: 20,
    addRemoveLinks: true,
});

$('#submit').click(function (e) {
    if (dropzoneThread.getQueuedFiles().length > 0) {
        e.preventDefault();
        e.stopPropagation();
        dropzoneThread.processQueue();
    } else {
        dropzoneThread.processQueue();
    }
});

dropzoneThread.on("success", function () {
    window.location.reload();
});

dropzoneThread.on("addedfiles", function () {
    if ($("#submit").is(":disabled")) {
        $("#submit").prop("disabled", false);
    }
})

dropzoneThread.on("removedfile", function () {
    if ($("#submit").is(":disabled") === false && this.getAcceptedFiles().length === 0)
        $("#submit").prop("disabled", true);
})

var dropWindow = $("#dropzoneArea");
var UploadIcon = $("#uploadIconDropzone");

function onDragOver(e) {
    dropWindow.show();
    dropWindow.css("border", "solid #D15C55");
    e.preventDefault();

}

function onDragEnter(e) {
    UploadIcon.css("display", "none");
    UploadIcon.css("visibility", "visible");
    dropWindow.css("border", "solid #D15C55");
}

function onDragLeave(e) {
    UploadIcon.css("display", "none");
    dropWindow.css("border", "solid #98DBAE");
}

function onDrop(e) {
    dropWindow.css("border", "dashed #13007C");
    UploadIcon.css("visibility", "visible");
    e.preventDefault();
    e.stopPropagation();
}

$(document).on('dragover', onDragOver);
$(document).on('dragenter', onDragEnter);
$(document).on('dragleave', onDragLeave);
$(document).on('drop', onDrop);

uploadIconDropzone.style.cursor = "pointer"

$("#dropzoneArea").hover(function () {
    $(this).find("#uploadIconDropzone").animate({
        opacity: 0.6,
    });
},
    function () {
        $(this).find("#uploadIconDropzone").animate({
            opacity: 1,
        });
    }
);

$("#dropzoneArea").click(function () {
    $(this).find("#uploadIconDropzone").css("display", "none")
});