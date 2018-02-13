  Vue.component("confirm-button",{
      props:["onConfirm", "confirmText", "event", "eventKey"],
      template:`<button @click="onClick"><slot></slot></button>`,
      methods:{
          onClick(){
             if (confirm(this.confirmText))
                 this.onConfirm(this.event, this.eventKey)
              }
           }
       });

