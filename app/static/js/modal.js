Vue.use(VeeValidate);

Vue.component('modal', {
  template: '#modal-template',
  delimiters: ['${', '}'],
  props: ['coords'],
  data: function() {
    return {
      title:'',
      description: '',
      image: '',
      eventTime: '',
      createdAt: '',
      formData: new FormData(),
      address: '',
      isAdded: 'none',
      tickets: [],
      savedTickets: [],
      validationErr: '',
      hasError: false,
      isAlert: false,
    }
  },
 methods: {
  loadEventData() {
    axios.get('/api/events', {'id': rootApp.userData.id })
      .then(resp => {
      console.log(this);
          this.eventData = resp.data;
          })
        .catch(err =>{console.log(err);});
  },
  onFileChange(e) {
    var files = e.target.files || e.dataTransfer.files;
    if (!files.length)
      return;

    this.createImage(files[0]);
  },
  createImage(file) {
    var image = new Image();
    var reader = new FileReader();
    var vm = this;
    this.formData.append('file', file);

   reader.onload = (e) => {
      vm.image = e.target.result;
    };
    reader.readAsDataURL(file);
  },
  removeImage: function (e) {
    this.image = '';
  },
  appendTicketForm: function() {
    this.tickets.push({
                        type: '',
                        price: '',
                        currency: '',
                        });
   },
  saveTicketType: function(type, price, currency) {
    this.savedTickets.push({'type': type, 'price': price, 'currency': currency });
  },
  removeTicketType: function(index) {
    this.tickets.splice(index, 1);
  },
  validateBeforeSubmit() {
    
    let self = this;

    this.$validator
      .validateAll()
      .then(function(response) {
          if(response){
            self.submitEvent();
            }
          })
      .catch(err => {
          });
  },
  submitEvent() {
    if(this.isAdded == 'inline') {
        this.formData.append('ticket', 'free');       
    }  
    this.formData.append('title', this.title);
    this.formData.append('description', this.description);
    this.formData.append('eventTime', this.eventTime);
    this.formData.append('createdAt', moment().toISOString());
    this.formData.append('fileName', 'Picture_' + moment().toISOString());
    this.formData.append('lat', this.coords.lat);
    this.formData.append('lng', this.coords.long);
    this.formData.append('savedTickets', JSON.stringify(this.savedTickets));

    let self = this;

    axios.post('/api/event', self.formData)
              .then(resp =>{
                    this.$nextTick(() => {
                    self.$emit('close');
                    self.formData = new FormData();
                    });
                  })
                   .catch(err => { 
                                   console.log(err);
                         }); 
         
  },
  closeModal() {
  console.log(this.coords);
    this.$emit('closemodal');
      }
    }
   });
