(self.webpackChunkzigate_plugin=self.webpackChunkzigate_plugin||[]).push([[902],{4902:(t,n,e)=>{"use strict";e.r(n),e.d(n,{SettingsModule:()=>O});var i=e(5425),s=e(3548),r=e(2548),a=e(1572),u=e(9774),c=e(3957),o=e(6073),l=e(5181),d=e(175),g=e(2582),_=e(1511),p=e(1980);function m(t,n){if(1&t&&(a.TgZ(0,"div",4),a._uU(1,"\n    "),a._UZ(2,"label",5),a._uU(3,"\n    "),a.TgZ(4,"div",6),a._uU(5,"\n      "),a._UZ(6,"input",7),a._uU(7,"\n    "),a.qZA(),a._uU(8,"\n  "),a.qZA()),2&t){const t=a.oxw(2);a.xp6(2),a.s9C("translate",t.setting.Name)}}function U(t,n){if(1&t&&(a.TgZ(0,"div",4),a._uU(1,"\n    "),a._UZ(2,"label",5),a._uU(3,"\n    "),a.TgZ(4,"div",6),a._uU(5,"\n      "),a._UZ(6,"input",7),a._uU(7,"\n    "),a.qZA(),a._uU(8,"\n  "),a.qZA()),2&t){const t=a.oxw(2);a.xp6(2),a.s9C("translate",t.setting.Name)}}function f(t,n){if(1&t&&(a.TgZ(0,"div",4),a._uU(1,"\n    "),a._UZ(2,"label",5),a._uU(3,"\n    "),a.TgZ(4,"div",6),a._uU(5,"\n      "),a._UZ(6,"input",8),a._uU(7,"\n    "),a.qZA(),a._uU(8,"\n  "),a.qZA()),2&t){const t=a.oxw(2);a.xp6(2),a.s9C("translate",t.setting.Name)}}function Z(t,n){if(1&t&&(a.TgZ(0,"div",4),a._uU(1,"\n    "),a._UZ(2,"label",5),a._uU(3,"\n    "),a.TgZ(4,"div",6),a._uU(5,"\n      "),a._UZ(6,"input",9),a._uU(7,"\n    "),a.qZA(),a._uU(8,"\n  "),a.qZA()),2&t){const t=a.oxw(2);a.xp6(2),a.s9C("translate",t.setting.Name)}}function h(t,n){if(1&t&&(a.TgZ(0,"div",4),a._uU(1,"\n    "),a._UZ(2,"label",5),a._uU(3,"\n    "),a.TgZ(4,"div",6),a._uU(5,"\n      "),a.TgZ(6,"ng-select",10),a._uU(7,"\n      "),a.qZA(),a._uU(8,"\n    "),a.qZA(),a._uU(9,"\n  "),a.qZA()),2&t){const t=a.oxw(2);a.xp6(2),a.s9C("translate",t.setting.Name),a.xp6(4),a.Q6J("items",t.list)("compareWith",t.compareNumeric)("closeOnSelect",!0)}}function v(t,n){if(1&t&&(a.TgZ(0,"div",11),a._uU(1,"\n    "),a._UZ(2,"input",12),a._uU(3,"\n    "),a._UZ(4,"label",13),a._uU(5,"\n  "),a.qZA()),2&t){const t=a.oxw(2);a.xp6(2),a.s9C("id",t.setting.Name),a.xp6(2),a.s9C("for",t.setting.Name),a.s9C("translate",t.setting.Name)}}function b(t,n){if(1&t&&(a.TgZ(0,"div",1),a._uU(1,"\n  "),a.YNc(2,m,9,1,"div",2),a._uU(3,"\n  "),a.YNc(4,U,9,1,"div",2),a._uU(5,"\n  "),a.YNc(6,f,9,1,"div",2),a._uU(7,"\n  "),a.YNc(8,Z,9,1,"div",2),a._uU(9,"\n  "),a.YNc(10,h,10,4,"div",2),a._uU(11,"\n  "),a.YNc(12,v,6,3,"div",3),a._uU(13,"\n"),a.qZA()),2&t){const t=a.oxw();a.Q6J("formGroupName",t.setting.Name),a.xp6(2),a.Q6J("ngIf","str"===t.setting.DataType),a.xp6(2),a.Q6J("ngIf","path"===t.setting.DataType),a.xp6(2),a.Q6J("ngIf","int"===t.setting.DataType),a.xp6(2),a.Q6J("ngIf","hex"===t.setting.DataType),a.xp6(2),a.Q6J("ngIf","list"===t.setting.DataType),a.xp6(2),a.Q6J("ngIf","bool"===t.setting.DataType)}}new r.Yd("SettingComponent");let T=(()=>{class t{constructor(t,n,e){this.formBuilder=t,this.fgd=n,this.translate=e,this.list=[]}ngOnChanges(t){let n;if(t.setting&&t.setting.currentValue){this.setting=t.setting.currentValue,"hex"===this.setting.DataType?n=this.formBuilder.group({current:["",o.kI.compose([o.kI.required,o.kI.pattern("^[0-9A-Fa-f]+")])]}):"bool"===this.setting.DataType?n=this.formBuilder.group({current:[]}):"list"===this.setting.DataType?(n=this.formBuilder.group({current:[null,o.kI.required]}),this.list=[],this.setting.list.forEach(t=>{const n=Object.keys(t)[0],e=Object.values(t)[0];this.list.push({label:n,value:e})})):n=this.formBuilder.group({current:["",o.kI.required]}),this.fgd.form.addControl(this.setting.Name,n);const e=""!==this.setting.current_value?this.setting.current_value:this.setting.default_value;this.fgd.form.get(this.setting.Name).get("current").patchValue(e)}}compareNumeric(t,n){return isNaN(t.value)?t.value===n:t.value===Number(n)}}return t.\u0275fac=function(n){return new(n||t)(a.Y36(o.qu),a.Y36(o.sg),a.Y36(g.sK))},t.\u0275cmp=a.Xpm({type:t,selectors:[["app-setting"]],inputs:{setting:"setting",advanced:"advanced"},features:[a._Bn([],[{provide:o.gN,useExisting:o.sg}]),a.TTD],decls:2,vars:1,consts:[[3,"formGroupName",4,"ngIf"],[3,"formGroupName"],["class","form-group row mt-2",4,"ngIf"],["class","row mt-2 custom-control custom-checkbox",4,"ngIf"],[1,"form-group","row","mt-2"],["for","current",1,"col-sm-6","col-form-label",3,"translate"],[1,"col-sm"],["type","text","formControlName","current",1,"w-100","form-control"],["type","number","formControlName","current",1,"w-50","form-control"],["type","text","formControlName","current",1,"w-50","form-control"],["bindLabel","label","bindValue","value","formControlName","current",3,"items","compareWith","closeOnSelect"],[1,"row","mt-2","custom-control","custom-checkbox"],["formControlName","current","type","checkbox",1,"custom-control-input","form-control",3,"id"],[1,"ml-3","custom-control-label",3,"for","translate"]],template:function(t,n){1&t&&(a.YNc(0,b,14,7,"div",0),a._uU(1,"\n")),2&t&&a.Q6J("ngIf",!1===n.setting.Advanced||n.advanced===n.setting.Advanced)},directives:[_.O5,o.JL,o.x0,g.Pi,o.Fj,o.JJ,o.u,o.wV,p.w9,o.Wl],styles:[".custom-control-input.is-valid[_ngcontent-%COMP%] ~ .custom-control-label[_ngcontent-%COMP%], was-validated[_ngcontent-%COMP%]   .custom-control-input[_ngcontent-%COMP%]:valid ~ .custom-control-label[_ngcontent-%COMP%]{color:#000}"]}),t})();const A=["contentRestart"];function q(t,n){if(1&t&&(a.ynx(0),a._uU(1,"\n                  "),a._UZ(2,"app-setting",28),a._uU(3,"\n                "),a.BQk()),2&t){const t=n.$implicit,e=a.oxw(4);a.xp6(2),a.Q6J("setting",t)("advanced",e.advanced)}}function x(t,n){if(1&t&&(a.TgZ(0,"div",22),a._uU(1,"\n            "),a._UZ(2,"div",23),a._uU(3,"\n            "),a.TgZ(4,"div",24),a._uU(5,"\n              "),a.TgZ(6,"div",25),a._uU(7,"\n                "),a._UZ(8,"h5",26),a._uU(9,"\n              "),a.qZA(),a._uU(10,"\n              "),a.TgZ(11,"div",27),a._uU(12,"\n                "),a.YNc(13,q,4,2,"ng-container",20),a._uU(14,"\n              "),a.qZA(),a._uU(15,"\n            "),a.qZA(),a._uU(16,"\n          "),a.qZA()),2&t){const t=a.oxw().$implicit,n=a.oxw(2);a.xp6(2),a.Q6J("innerHTML",n.getTranslation("setting.header.",t._Theme),a.oJD),a.xp6(6),a.Q6J("innerHTML",n.getTranslation("setting.subtitle.",t._Theme),a.oJD),a.xp6(5),a.Q6J("ngForOf",t.ListOfSettings)}}function N(t,n){if(1&t&&(a.TgZ(0,"div"),a._uU(1,"\n          "),a.YNc(2,x,17,3,"div",21),a._uU(3,"\n        "),a.qZA()),2&t){const t=n.$implicit,e=a.oxw(2);a.xp6(2),a.Q6J("ngIf",e.hasBasicSettings(t.ListOfSettings))}}function k(t,n){if(1&t){const t=a.EpF();a.TgZ(0,"form",4),a._uU(1,"\n  "),a.TgZ(2,"fieldset",5),a._uU(3,"\n    "),a.TgZ(4,"legend"),a._uU(5,"\n      "),a.TgZ(6,"div",6),a._uU(7,"\n        "),a._UZ(8,"div",7),a.ALo(9,"translate"),a._uU(10,"\n        "),a.TgZ(11,"div",8),a._uU(12,"\n          "),a.TgZ(13,"div",9),a._uU(14,"\n            "),a.TgZ(15,"div",10),a._uU(16,"\n              "),a.TgZ(17,"button",11),a.NdJ("click",function(){return a.CHM(t),a.oxw().updateSettings()}),a.qZA(),a._uU(18,"\n            "),a.qZA(),a._uU(19,"\n            "),a.TgZ(20,"div",12),a._uU(21,"\n              "),a.TgZ(22,"button",13),a.NdJ("click",function(){return a.CHM(t),a.oxw().reinitSettings()}),a.qZA(),a._uU(23,"\n            "),a.qZA(),a._uU(24,"\n            "),a.TgZ(25,"div",14),a._uU(26,"\n              "),a.TgZ(27,"input",15),a.NdJ("click",function(n){return a.CHM(t),a.oxw().advancedSettings(n)}),a.qZA(),a._uU(28,"\n              "),a._UZ(29,"label",16),a._uU(30,"\n            "),a.qZA(),a._uU(31,"\n          "),a.qZA(),a._uU(32,"\n        "),a.qZA(),a._uU(33,"\n      "),a.qZA(),a._uU(34,"\n    "),a.qZA(),a._uU(35,"\n    "),a._UZ(36,"h5",17),a.ALo(37,"translate"),a._uU(38,"\n  "),a.qZA(),a._uU(39,"\n  "),a.TgZ(40,"div",18),a._uU(41,"\n    "),a.TgZ(42,"div",6),a._uU(43,"\n      "),a.TgZ(44,"div",19),a._uU(45,"\n        "),a.YNc(46,N,4,1,"div",20),a._uU(47,"\n      "),a.qZA(),a._uU(48,"\n    "),a.qZA(),a._uU(49,"\n  "),a.qZA(),a._uU(50,"\n"),a.qZA()}if(2&t){const t=a.oxw();a.Q6J("formGroup",t.form),a.xp6(8),a.Q6J("innerHTML",a.lcZ(9,6,"setting.help.legend"),a.oJD),a.xp6(9),a.Q6J("disabled",!t.form.valid),a.xp6(10),a.Q6J("checked",t.advanced),a.xp6(9),a.Q6J("innerHTML",a.lcZ(37,8,"setting.help.link"),a.oJD),a.xp6(10),a.Q6J("ngForOf",t.settings)}}function w(t,n){1&t&&(a._uU(0,"\n  "),a.TgZ(1,"div",29),a._uU(2,"\n    "),a._UZ(3,"h4",30),a._uU(4,"\n    "),a.TgZ(5,"button",31),a.NdJ("click",function(){return n.$implicit.dismiss("Cross click")}),a._uU(6,"\n      "),a.TgZ(7,"span",32),a._uU(8,"\xd7"),a.qZA(),a._uU(9,"\n    "),a.qZA(),a._uU(10,"\n  "),a.qZA(),a._uU(11,"\n  "),a._UZ(12,"div",33),a._uU(13,"\n  "),a.TgZ(14,"div",34),a._uU(15,"\n    "),a.TgZ(16,"button",35),a.NdJ("click",function(){return n.$implicit.dismiss("cancel")}),a.qZA(),a._uU(17,"\n  "),a.qZA(),a._uU(18,"\n"))}function J(t,n){1&t&&(a._uU(0,"\n  "),a.TgZ(1,"div",29),a._uU(2,"\n    "),a._UZ(3,"h4",36),a._uU(4,"\n    "),a.TgZ(5,"button",31),a.NdJ("click",function(){return n.$implicit.dismiss("Cross click")}),a._uU(6,"\n      "),a.TgZ(7,"span",32),a._uU(8,"\xd7"),a.qZA(),a._uU(9,"\n    "),a.qZA(),a._uU(10,"\n  "),a.qZA(),a._uU(11,"\n  "),a._UZ(12,"div",37),a._uU(13,"\n  "),a.TgZ(14,"div",34),a._uU(15,"\n    "),a.TgZ(16,"button",38),a.NdJ("click",function(){return n.$implicit.dismiss("cancel")}),a.qZA(),a._uU(17,"\n  "),a.qZA(),a._uU(18,"\n"))}function y(t,n){1&t&&(a._uU(0,"\n  "),a.TgZ(1,"div",29),a._uU(2,"\n    "),a._UZ(3,"h4",39),a._uU(4,"\n    "),a.TgZ(5,"button",31),a.NdJ("click",function(){return n.$implicit.dismiss("Cross click")}),a._uU(6,"\n      "),a.TgZ(7,"span",32),a._uU(8,"\xd7"),a.qZA(),a._uU(9,"\n    "),a.qZA(),a._uU(10,"\n  "),a.qZA(),a._uU(11,"\n  "),a._UZ(12,"div",40),a._uU(13,"\n  "),a.TgZ(14,"div",34),a._uU(15,"\n    "),a.TgZ(16,"button",41),a.NdJ("click",function(){return n.$implicit.dismiss("cancel")}),a.qZA(),a._uU(17,"\n  "),a.qZA(),a._uU(18,"\n"))}new r.Yd("SettingsComponent");const C=[{path:"",component:(()=>{class t{constructor(t,n,e,i,s,r){this.modalService=t,this.apiService=n,this.formBuilder=e,this.toastr=i,this.headerService=s,this.translate=r,this.advanced=!1}ngOnInit(){this.form=this.formBuilder.group({}),this.apiService.getSettings().subscribe(t=>{this.settings=t,this.settings.sort((t,n)=>t._Order-n._Order)})}reinitSettings(){this.settings.forEach(t=>{const n=[];t.ListOfSettings.forEach(t=>{"path"!==t.DataType&&(t.current_value=t.default_value),n.push(Object.assign({},t))}),t.ListOfSettings=n}),this.settings=[...this.settings],this.form.markAsTouched()}advancedSettings(t){this.advanced=!!t.currentTarget.checked}updateSettings(){this.form.invalid?this.form.markAsTouched():(Object.keys(this.form.value).forEach(t=>{!0===this.form.value[t].current?this.form.value[t].current=1:!1===this.form.value[t].current&&(this.form.value[t].current=0)}),this.apiService.putSettings(this.form.value).subscribe(t=>{this.form.markAsPristine(),this.toastr.success(this.translate.instant("api.global.succes.update.title")),this.apiService.getSettings().subscribe(t=>{this.settings=t,this.settings.sort((t,n)=>t._Order-n._Order)}),this.apiService.getRestartNeeded().subscribe(t=>{1===t.RestartNeeded?(this.headerService.setRestart(!0),this.open(this.contentRestart)):2===t.RestartNeeded?this.open(this.contentReset):3===t.RestartNeeded&&this.open(this.contentErase)})}))}open(t){this.modalService.open(t,{ariaLabelledBy:"modal-basic-title"}).result.then(t=>{},t=>{})}hasBasicSettings(t){return!!this.advanced||t.filter(t=>!1===t.Advanced).length>0}getTranslation(t,n){return this.translate.instant(t.concat(n))}}return t.\u0275fac=function(n){return new(n||t)(a.Y36(u.FF),a.Y36(c.s),a.Y36(o.qu),a.Y36(l._W),a.Y36(d.r),a.Y36(g.sK))},t.\u0275cmp=a.Xpm({type:t,selectors:[["app-settings"]],viewQuery:function(t,n){if(1&t&&(a.Gf(A,5),a.Gf(A,5),a.Gf(A,5)),2&t){let t;a.iGM(t=a.CRH())&&(n.contentRestart=t.first),a.iGM(t=a.CRH())&&(n.contentReset=t.first),a.iGM(t=a.CRH())&&(n.contentErase=t.first)}},decls:11,vars:1,consts:[[3,"formGroup",4,"ngIf"],["contentRestart",""],["contentReset",""],["contentErase",""],[3,"formGroup"],[1,"h-100"],[1,"row"],[1,"col-sm-8",3,"innerHTML"],[1,"col-sm-4"],[1,"d-flex","flex-row-reverse","align-items-center"],[1,"p-2"],["translate","setting.validate.button",1,"btn","btn-primary",3,"disabled","click"],[1,"p-2","ml-3"],["translate","setting.reinit.button",1,"btn","btn-secondary",3,"click"],[1,"switch","switch-sm"],["type","checkbox","id","switch-advanced",1,"switch",3,"checked","click"],["for","switch-advanced","translate","setting.advanced.button",1,"mb-0"],[1,"card-title",3,"innerHTML"],[1,"mt-3"],[1,"col-sm-12","card-columns"],[4,"ngFor","ngForOf"],["class","card",4,"ngIf"],[1,"card"],[1,"card-header",3,"innerHTML"],[1,"card-body"],[1,"card-title"],[3,"innerHTML"],[1,"card-text"],[3,"setting","advanced"],[1,"modal-header"],["id","modal-basic-title","translate","setting.reloadplugin.alert.title",1,"modal-title"],["type","button","aria-label","Close",1,"close",3,"click"],["aria-hidden","true"],["translate","setting.reloadplugin.alert.subject",1,"modal-body"],[1,"modal-footer"],["type","button","translate","setting.reloadplugin.alert.cancel",1,"btn","btn-outline-dark",3,"click"],["id","modal-basic-title","translate","setting.resetplugin.alert.title",1,"modal-title"],["translate","setting.resetplugin.alert.subject",1,"modal-body"],["type","button","translate","setting.resetplugin.alert.cancel",1,"btn","btn-outline-dark",3,"click"],["id","modal-basic-title","translate","setting.eraseplugin.alert.title",1,"modal-title"],["translate","setting.eraseplugin.alert.subject",1,"modal-body"],["type","button","translate","setting.eraseplugin.alert.cancel",1,"btn","btn-outline-dark",3,"click"]],template:function(t,n){1&t&&(a.YNc(0,k,51,10,"form",0),a._uU(1,"\n\n"),a.YNc(2,w,19,0,"ng-template",null,1,a.W1O),a._uU(4,"\n\n"),a.YNc(5,J,19,0,"ng-template",null,2,a.W1O),a._uU(7,"\n\n"),a.YNc(8,y,19,0,"ng-template",null,3,a.W1O),a._uU(10,"\n")),2&t&&a.Q6J("ngIf",n.settings)},directives:[_.O5,o._Y,o.JL,o.sg,g.Pi,_.sg,T],pipes:[g.X$],styles:[""]}),t})(),data:{title:(0,r.Kl)("settings")}}];let S=(()=>{class t{}return t.\u0275fac=function(n){return new(n||t)},t.\u0275mod=a.oAB({type:t}),t.\u0275inj=a.cJS({providers:[],imports:[[s.Bz.forChild(C)],s.Bz]}),t})(),O=(()=>{class t{}return t.\u0275fac=function(n){return new(n||t)},t.\u0275mod=a.oAB({type:t}),t.\u0275inj=a.cJS({imports:[[S,i.m]]}),t})()}}]);