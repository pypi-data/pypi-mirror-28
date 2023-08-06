var store = {
    state: {}
}

Vue.component('upload-progress', {
    template: '#upload-progress-template',
    delimiters: ['${', '}'],
    props: ['files'],
    methods: {
        removeFile(file) {
            this.files.forEach((f, index) => {
                if (f.id === file.id) {
                    this.files.splice(index, 1)
                }
            })
        }
    }
})

Vue.component('upload-progress-item', {
    template: '#upload-progress-item-template',
    delimiters: ['${', '}'],
    props: ['file'],
    data: {},
    methods: {
        remove() {
            this.$emit('remove', this.file)
        }
    }
})

Vue.component('upload-dnd', {
    template: '#upload-dnd-template',
    delimiters: ['${', '}'],
    data() {
        return {
            isOver: false
        }
    },
    methods: {
        onDrop(event) {
            var files = event.dataTransfer.files;
            this.$emit('newFiles', files)
        },
        onDragEnter() {
            this.isOver = true
        },
        onDragLeave() {
            this.isOver = false
        },
        onDragOver() {}
    }
});


var Uploader2S3Vue = Vue.extend({
    el: '#uploader',
    template: '#uploader-template',
    delimiters: ['${', '}'],
    data() {
        return {
            files: [
                // {
                //       _id: 12,
                //       percentage: 90,
                //       file: {
                //         name: '1516697920464 bip_cadbip_SP_003_TestBIP003.zip'
                //     },
                //     error: 'sdjshjshd'
                // },
                //     {
                //       _id: 13,
                //       percentage: 24,
                //       file: {
                //         name: '1516697920464 bip_cadbip_SP_003_Pepito.zip'
                //     },
                //     error: 'wooooop'
                //     }
            ],
            config: {
                'url': '{{ s3_credentials.url }}',
                'policy': '{{ s3_credentials.policy }}',
                'Content-Type': '{{ s3_credentials.content_type }}',
                'acl': '{{ s3_credentials.acl }}',
                'success_action_status': '{{ s3_credentials.success_action_status }}',
                'X-amz-credential': '{{ s3_credentials.x_amz_credential }}',
                'X-amz-algorithm': '{{ s3_credentials.x_amz_algorithm }}',
                'X-amz-date': '{{ s3_credentials.x_amz_date }}',
                'X-amz-signature': '{{ s3_credentials.x_amz_signature }}',
            },
            sharedState: store.state
        }
    },
    methods: {
        getUploadFilename(file) {
            return file.name;
        },
        callback(data) {},
        newDndFiles(files) {
            let newFiles = Array.from(files);
            this.uploadFiles(newFiles);
        },
        newFormFiles(event) {
            let newFiles = Array.from(event.target.files);
            this.uploadFiles(newFiles);
        },
        uploadFiles(files) {
            files.forEach(file => {
                var newFile = {
                    _id: Date.now(),
                    percentage: 0,
                    file: file,
                    error: null
                }
                this.files.push(newFile);
                this.upload(newFile);
            })
        },
        upload: function(newFile) {
            let file = newFile.file
            var formData = new FormData();
            formData.append('policy', this.config['policy']);
            formData.append('Content-Type', this.config['Content-Type']);
            formData.append('acl', this.config['acl']);
            formData.append('success_action_status', this.config['success_action_status']);
            formData.append('X-amz-credential', this.config['X-amz-credential']);
            formData.append('X-amz-algorithm', this.config['X-amz-algorithm']);
            formData.append('X-amz-date', this.config['X-amz-date']);
            formData.append('X-amz-signature', this.config['X-amz-signature']);

            let filename;
            try {
                filename = this.getUploadFilename(file)
            } catch (e) {
                newFile.error = e;
                return false;
            }
            formData.append('key', filename);
            formData.append('file', file);

            let config = {
                responseType: 'document',
                onUploadProgress: progressEvent => {
                    let percentCompleted = Math.floor(
                        (progressEvent.loaded * 100) / progressEvent.total);
                    newFile.percentage = percentCompleted;
                }
            };

            axios.post(this.config.url, formData, config)
                .then(response => {
                    newFile.percentage = 100;
                    var s3Result = response.data.documentElement.children;
                    var result = {
                        "original_name": newFile.file.name,
                        "s3_name": s3Result[2].innerHTML,
                        "size": newFile.file.size,
                        "url": s3Result[0].innerHTML.replace("%2F", "/")
                    };
                    this.callback(result);
                })
                .catch(e => {
                    var error = "{% trans 'Data error' %}";
                    if (e.request && e.request.status >= 400 &&
                        e.request.status < 500) {
                        error = "{% trans 'incorrect parameters' %}";
                    }
                    if (e.request && e.request.status > 500) {
                        error = "{% trans 'server error' %}";
                    }
                    newFile.error = error;
                    console.log(e);
                });
        }
    }
});
