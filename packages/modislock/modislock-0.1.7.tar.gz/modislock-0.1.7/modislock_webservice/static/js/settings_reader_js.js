/*! ========================================================================
 * Bootstrap Toggle: bootstrap-toggle.js v2.2.0
 * http://www.bootstraptoggle.com
 * ========================================================================
 * Copyright 2014 Min Hur, The New York Times Company
 * Licensed under MIT
 * ======================================================================== */
+function($){'use strict';var Toggle=function(element,options){this.$element=$(element)
this.options=$.extend({},this.defaults(),options)
this.render()}
Toggle.VERSION='2.2.0'
Toggle.DEFAULTS={on:'On',off:'Off',onstyle:'primary',offstyle:'default',size:'normal',style:'',width:null,height:null}
Toggle.prototype.defaults=function(){return{on:this.$element.attr('data-on')||Toggle.DEFAULTS.on,off:this.$element.attr('data-off')||Toggle.DEFAULTS.off,onstyle:this.$element.attr('data-onstyle')||Toggle.DEFAULTS.onstyle,offstyle:this.$element.attr('data-offstyle')||Toggle.DEFAULTS.offstyle,size:this.$element.attr('data-size')||Toggle.DEFAULTS.size,style:this.$element.attr('data-style')||Toggle.DEFAULTS.style,width:this.$element.attr('data-width')||Toggle.DEFAULTS.width,height:this.$element.attr('data-height')||Toggle.DEFAULTS.height}}
Toggle.prototype.render=function(){this._onstyle='btn-'+this.options.onstyle
this._offstyle='btn-'+this.options.offstyle
var size=this.options.size==='large'?'btn-lg':this.options.size==='small'?'btn-sm':this.options.size==='mini'?'btn-xs':''
var $toggleOn=$('<label class="btn">').html(this.options.on).addClass(this._onstyle+' '+size)
var $toggleOff=$('<label class="btn">').html(this.options.off).addClass(this._offstyle+' '+size+' active')
var $toggleHandle=$('<span class="toggle-handle btn btn-default">').addClass(size)
var $toggleGroup=$('<div class="toggle-group">').append($toggleOn,$toggleOff,$toggleHandle)
var $toggle=$('<div class="toggle btn" data-toggle="toggle">').addClass(this.$element.prop('checked')?this._onstyle:this._offstyle+' off').addClass(size).addClass(this.options.style)
this.$element.wrap($toggle)
$.extend(this,{$toggle:this.$element.parent(),$toggleOn:$toggleOn,$toggleOff:$toggleOff,$toggleGroup:$toggleGroup})
this.$toggle.append($toggleGroup)
var width=this.options.width||Math.max($toggleOn.outerWidth(),$toggleOff.outerWidth())+($toggleHandle.outerWidth()/2)
var height=this.options.height||Math.max($toggleOn.outerHeight(),$toggleOff.outerHeight())
$toggleOn.addClass('toggle-on')
$toggleOff.addClass('toggle-off')
this.$toggle.css({width:width,height:height})
if(this.options.height){$toggleOn.css('line-height',$toggleOn.height()+'px')
$toggleOff.css('line-height',$toggleOff.height()+'px')}
this.update(true)
this.trigger(true)}
Toggle.prototype.toggle=function(){if(this.$element.prop('checked'))this.off()
else this.on()}
Toggle.prototype.on=function(silent){if(this.$element.prop('disabled'))return false
this.$toggle.removeClass(this._offstyle+' off').addClass(this._onstyle)
this.$element.prop('checked',true)
if(!silent)this.trigger()}
Toggle.prototype.off=function(silent){if(this.$element.prop('disabled'))return false
this.$toggle.removeClass(this._onstyle).addClass(this._offstyle+' off')
this.$element.prop('checked',false)
if(!silent)this.trigger()}
Toggle.prototype.enable=function(){this.$toggle.removeAttr('disabled')
this.$element.prop('disabled',false)}
Toggle.prototype.disable=function(){this.$toggle.attr('disabled','disabled')
this.$element.prop('disabled',true)}
Toggle.prototype.update=function(silent){if(this.$element.prop('disabled'))this.disable()
else this.enable()
if(this.$element.prop('checked'))this.on(silent)
else this.off(silent)}
Toggle.prototype.trigger=function(silent){this.$element.off('change.bs.toggle')
if(!silent)this.$element.change()
this.$element.on('change.bs.toggle',$.proxy(function(){this.update()},this))}
Toggle.prototype.destroy=function(){this.$element.off('change.bs.toggle')
this.$toggleGroup.remove()
this.$element.removeData('bs.toggle')
this.$element.unwrap()}
function Plugin(option){return this.each(function(){var $this=$(this)
var data=$this.data('bs.toggle')
var options=typeof option=='object'&&option
if(!data)$this.data('bs.toggle',(data=new Toggle(this,options)))
if(typeof option=='string'&&data[option])data[option]()})}
var old=$.fn.bootstrapToggle
$.fn.bootstrapToggle=Plugin
$.fn.bootstrapToggle.Constructor=Toggle
$.fn.toggle.noConflict=function(){$.fn.bootstrapToggle=old
return this}
$(function(){$('input[type=checkbox][data-toggle^=toggle]').bootstrapToggle()})
$(document).on('click.bs.toggle','div[data-toggle^=toggle]',function(e){var $checkbox=$(this).find('input[type=checkbox]')
$checkbox.bootstrapToggle('toggle')
e.preventDefault()})}(jQuery);(function($){'use strict';var _currentSpinnerId=0;function _scopedEventName(name,id){return name+'.touchspin_'+id;}
function _scopeEventNames(names,id){return $.map(names,function(name){return _scopedEventName(name,id);});}
$.fn.TouchSpin=function(options){if(options==='destroy'){this.each(function(){var originalinput=$(this),originalinput_data=originalinput.data();$(document).off(_scopeEventNames(['mouseup','touchend','touchcancel','mousemove','touchmove','scroll','scrollstart'],originalinput_data.spinnerid).join(' '));});return;}
var defaults={min:0,max:100,initval:'',replacementval:'',step:1,decimals:0,stepinterval:100,forcestepdivisibility:'round',stepintervaldelay:500,verticalbuttons:false,verticalupclass:'glyphicon glyphicon-chevron-up',verticaldownclass:'glyphicon glyphicon-chevron-down',prefix:'',postfix:'',prefix_extraclass:'',postfix_extraclass:'',booster:true,boostat:10,maxboostedstep:false,mousewheel:true,buttondown_class:'btn btn-default',buttonup_class:'btn btn-default',buttondown_txt:'-',buttonup_txt:'+'};var attributeMap={min:'min',max:'max',initval:'init-val',replacementval:'replacement-val',step:'step',decimals:'decimals',stepinterval:'step-interval',verticalbuttons:'vertical-buttons',verticalupclass:'vertical-up-class',verticaldownclass:'vertical-down-class',forcestepdivisibility:'force-step-divisibility',stepintervaldelay:'step-interval-delay',prefix:'prefix',postfix:'postfix',prefix_extraclass:'prefix-extra-class',postfix_extraclass:'postfix-extra-class',booster:'booster',boostat:'boostat',maxboostedstep:'max-boosted-step',mousewheel:'mouse-wheel',buttondown_class:'button-down-class',buttonup_class:'button-up-class',buttondown_txt:'button-down-txt',buttonup_txt:'button-up-txt'};return this.each(function(){var settings,originalinput=$(this),originalinput_data=originalinput.data(),container,elements,value,downSpinTimer,upSpinTimer,downDelayTimeout,upDelayTimeout,spincount=0,spinning=false;init();function init(){if(originalinput.data('alreadyinitialized')){return;}
originalinput.data('alreadyinitialized',true);_currentSpinnerId+=1;originalinput.data('spinnerid',_currentSpinnerId);if(!originalinput.is('input')){console.log('Must be an input.');return;}
_initSettings();_setInitval();_checkValue();_buildHtml();_initElements();_hideEmptyPrefixPostfix();_bindEvents();_bindEventsInterface();elements.input.css('display','block');}
function _setInitval(){if(settings.initval!==''&&originalinput.val()===''){originalinput.val(settings.initval);}}
function changeSettings(newsettings){_updateSettings(newsettings);_checkValue();var value=elements.input.val();if(value!==''){value=Number(elements.input.val());elements.input.val(value.toFixed(settings.decimals));}}
function _initSettings(){settings=$.extend({},defaults,originalinput_data,_parseAttributes(),options);}
function _parseAttributes(){var data={};$.each(attributeMap,function(key,value){var attrName='bts-'+value+'';if(originalinput.is('[data-'+attrName+']')){data[key]=originalinput.data(attrName);}});return data;}
function _updateSettings(newsettings){settings=$.extend({},settings,newsettings);if(newsettings.postfix){originalinput.parent().find('.bootstrap-touchspin-postfix').text(newsettings.postfix);}
if(newsettings.prefix){originalinput.parent().find('.bootstrap-touchspin-prefix').text(newsettings.prefix);}}
function _buildHtml(){var initval=originalinput.val(),parentelement=originalinput.parent();if(initval!==''){initval=Number(initval).toFixed(settings.decimals);}
originalinput.data('initvalue',initval).val(initval);originalinput.addClass('form-control');if(parentelement.hasClass('input-group')){_advanceInputGroup(parentelement);}
else{_buildInputGroup();}}
function _advanceInputGroup(parentelement){parentelement.addClass('bootstrap-touchspin');var prev=originalinput.prev(),next=originalinput.next();var downhtml,uphtml,prefixhtml='<span class="input-group-addon bootstrap-touchspin-prefix">'+settings.prefix+'</span>',postfixhtml='<span class="input-group-addon bootstrap-touchspin-postfix">'+settings.postfix+'</span>';if(prev.hasClass('input-group-btn')){downhtml='<button class="'+settings.buttondown_class+' bootstrap-touchspin-down" type="button">'+settings.buttondown_txt+'</button>';prev.append(downhtml);}
else{downhtml='<span class="input-group-btn"><button class="'+settings.buttondown_class+' bootstrap-touchspin-down" type="button">'+settings.buttondown_txt+'</button></span>';$(downhtml).insertBefore(originalinput);}
if(next.hasClass('input-group-btn')){uphtml='<button class="'+settings.buttonup_class+' bootstrap-touchspin-up" type="button">'+settings.buttonup_txt+'</button>';next.prepend(uphtml);}
else{uphtml='<span class="input-group-btn"><button class="'+settings.buttonup_class+' bootstrap-touchspin-up" type="button">'+settings.buttonup_txt+'</button></span>';$(uphtml).insertAfter(originalinput);}
$(prefixhtml).insertBefore(originalinput);$(postfixhtml).insertAfter(originalinput);container=parentelement;}
function _buildInputGroup(){var html;if(settings.verticalbuttons){html='<div class="input-group bootstrap-touchspin"><span class="input-group-addon bootstrap-touchspin-prefix">'+settings.prefix+'</span><span class="input-group-addon bootstrap-touchspin-postfix">'+settings.postfix+'</span><span class="input-group-btn-vertical"><button class="'+settings.buttondown_class+' bootstrap-touchspin-up" type="button"><i class="'+settings.verticalupclass+'"></i></button><button class="'+settings.buttonup_class+' bootstrap-touchspin-down" type="button"><i class="'+settings.verticaldownclass+'"></i></button></span></div>';}
else{html='<div class="input-group bootstrap-touchspin"><span class="input-group-btn"><button class="'+settings.buttondown_class+' bootstrap-touchspin-down" type="button">'+settings.buttondown_txt+'</button></span><span class="input-group-addon bootstrap-touchspin-prefix">'+settings.prefix+'</span><span class="input-group-addon bootstrap-touchspin-postfix">'+settings.postfix+'</span><span class="input-group-btn"><button class="'+settings.buttonup_class+' bootstrap-touchspin-up" type="button">'+settings.buttonup_txt+'</button></span></div>';}
container=$(html).insertBefore(originalinput);$('.bootstrap-touchspin-prefix',container).after(originalinput);if(originalinput.hasClass('input-sm')){container.addClass('input-group-sm');}
else if(originalinput.hasClass('input-lg')){container.addClass('input-group-lg');}}
function _initElements(){elements={down:$('.bootstrap-touchspin-down',container),up:$('.bootstrap-touchspin-up',container),input:$('input',container),prefix:$('.bootstrap-touchspin-prefix',container).addClass(settings.prefix_extraclass),postfix:$('.bootstrap-touchspin-postfix',container).addClass(settings.postfix_extraclass)};}
function _hideEmptyPrefixPostfix(){if(settings.prefix===''){elements.prefix.hide();}
if(settings.postfix===''){elements.postfix.hide();}}
function _bindEvents(){originalinput.on('keydown',function(ev){var code=ev.keyCode||ev.which;if(code===38){if(spinning!=='up'){upOnce();startUpSpin();}
ev.preventDefault();}
else if(code===40){if(spinning!=='down'){downOnce();startDownSpin();}
ev.preventDefault();}});originalinput.on('keyup',function(ev){var code=ev.keyCode||ev.which;if(code===38){stopSpin();}
else if(code===40){stopSpin();}});originalinput.on('blur',function(){_checkValue();});elements.down.on('keydown',function(ev){var code=ev.keyCode||ev.which;if(code===32||code===13){if(spinning!=='down'){downOnce();startDownSpin();}
ev.preventDefault();}});elements.down.on('keyup',function(ev){var code=ev.keyCode||ev.which;if(code===32||code===13){stopSpin();}});elements.up.on('keydown',function(ev){var code=ev.keyCode||ev.which;if(code===32||code===13){if(spinning!=='up'){upOnce();startUpSpin();}
ev.preventDefault();}});elements.up.on('keyup',function(ev){var code=ev.keyCode||ev.which;if(code===32||code===13){stopSpin();}});elements.down.on('mousedown.touchspin',function(ev){elements.down.off('touchstart.touchspin');if(originalinput.is(':disabled')){return;}
downOnce();startDownSpin();ev.preventDefault();ev.stopPropagation();});elements.down.on('touchstart.touchspin',function(ev){elements.down.off('mousedown.touchspin');if(originalinput.is(':disabled')){return;}
downOnce();startDownSpin();ev.preventDefault();ev.stopPropagation();});elements.up.on('mousedown.touchspin',function(ev){elements.up.off('touchstart.touchspin');if(originalinput.is(':disabled')){return;}
upOnce();startUpSpin();ev.preventDefault();ev.stopPropagation();});elements.up.on('touchstart.touchspin',function(ev){elements.up.off('mousedown.touchspin');if(originalinput.is(':disabled')){return;}
upOnce();startUpSpin();ev.preventDefault();ev.stopPropagation();});elements.up.on('mouseout touchleave touchend touchcancel',function(ev){if(!spinning){return;}
ev.stopPropagation();stopSpin();});elements.down.on('mouseout touchleave touchend touchcancel',function(ev){if(!spinning){return;}
ev.stopPropagation();stopSpin();});elements.down.on('mousemove touchmove',function(ev){if(!spinning){return;}
ev.stopPropagation();ev.preventDefault();});elements.up.on('mousemove touchmove',function(ev){if(!spinning){return;}
ev.stopPropagation();ev.preventDefault();});$(document).on(_scopeEventNames(['mouseup','touchend','touchcancel'],_currentSpinnerId).join(' '),function(ev){if(!spinning){return;}
ev.preventDefault();stopSpin();});$(document).on(_scopeEventNames(['mousemove','touchmove','scroll','scrollstart'],_currentSpinnerId).join(' '),function(ev){if(!spinning){return;}
ev.preventDefault();stopSpin();});originalinput.on('mousewheel DOMMouseScroll',function(ev){if(!settings.mousewheel||!originalinput.is(':focus')){return;}
var delta=ev.originalEvent.wheelDelta||-ev.originalEvent.deltaY||-ev.originalEvent.detail;ev.stopPropagation();ev.preventDefault();if(delta<0){downOnce();}
else{upOnce();}});}
function _bindEventsInterface(){originalinput.on('touchspin.uponce',function(){stopSpin();upOnce();});originalinput.on('touchspin.downonce',function(){stopSpin();downOnce();});originalinput.on('touchspin.startupspin',function(){startUpSpin();});originalinput.on('touchspin.startdownspin',function(){startDownSpin();});originalinput.on('touchspin.stopspin',function(){stopSpin();});originalinput.on('touchspin.updatesettings',function(e,newsettings){changeSettings(newsettings);});}
function _forcestepdivisibility(value){switch(settings.forcestepdivisibility){case'round':return(Math.round(value/settings.step)*settings.step).toFixed(settings.decimals);case'floor':return(Math.floor(value/settings.step)*settings.step).toFixed(settings.decimals);case'ceil':return(Math.ceil(value/settings.step)*settings.step).toFixed(settings.decimals);default:return value;}}
function _checkValue(){var val,parsedval,returnval;val=originalinput.val();if(val===''){if(settings.replacementval!==''){originalinput.val(settings.replacementval);originalinput.trigger('change');}
return;}
if(settings.decimals>0&&val==='.'){return;}
parsedval=parseFloat(val);if(isNaN(parsedval)){if(settings.replacementval!==''){parsedval=settings.replacementval;}
else{parsedval=0;}}
returnval=parsedval;if(parsedval.toString()!==val){returnval=parsedval;}
if(parsedval<settings.min){returnval=settings.min;}
if(parsedval>settings.max){returnval=settings.max;}
returnval=_forcestepdivisibility(returnval);if(Number(val).toString()!==returnval.toString()){originalinput.val(returnval);originalinput.trigger('change');}}
function _getBoostedStep(){if(!settings.booster){return settings.step;}
else{var boosted=Math.pow(2,Math.floor(spincount/settings.boostat))*settings.step;if(settings.maxboostedstep){if(boosted>settings.maxboostedstep){boosted=settings.maxboostedstep;value=Math.round((value/boosted))*boosted;}}
return Math.max(settings.step,boosted);}}
function upOnce(){_checkValue();value=parseFloat(elements.input.val());if(isNaN(value)){value=0;}
var initvalue=value,boostedstep=_getBoostedStep();value=value+boostedstep;if(value>settings.max){value=settings.max;originalinput.trigger('touchspin.on.max');stopSpin();}
elements.input.val(Number(value).toFixed(settings.decimals));if(initvalue!==value){originalinput.trigger('change');}}
function downOnce(){_checkValue();value=parseFloat(elements.input.val());if(isNaN(value)){value=0;}
var initvalue=value,boostedstep=_getBoostedStep();value=value-boostedstep;if(value<settings.min){value=settings.min;originalinput.trigger('touchspin.on.min');stopSpin();}
elements.input.val(value.toFixed(settings.decimals));if(initvalue!==value){originalinput.trigger('change');}}
function startDownSpin(){stopSpin();spincount=0;spinning='down';originalinput.trigger('touchspin.on.startspin');originalinput.trigger('touchspin.on.startdownspin');downDelayTimeout=setTimeout(function(){downSpinTimer=setInterval(function(){spincount++;downOnce();},settings.stepinterval);},settings.stepintervaldelay);}
function startUpSpin(){stopSpin();spincount=0;spinning='up';originalinput.trigger('touchspin.on.startspin');originalinput.trigger('touchspin.on.startupspin');upDelayTimeout=setTimeout(function(){upSpinTimer=setInterval(function(){spincount++;upOnce();},settings.stepinterval);},settings.stepintervaldelay);}
function stopSpin(){clearTimeout(downDelayTimeout);clearTimeout(upDelayTimeout);clearInterval(downSpinTimer);clearInterval(upSpinTimer);switch(spinning){case'up':originalinput.trigger('touchspin.on.stopupspin');originalinput.trigger('touchspin.on.stopspin');break;case'down':originalinput.trigger('touchspin.on.stopdownspin');originalinput.trigger('touchspin.on.stopspin');break;}
spincount=0;spinning=false;}});};})(jQuery);(function(){$("#relay_1_delay").TouchSpin({min:500,max:5000,step:100,decimals:0,postfix:'ms'});$("#relay_2_delay").TouchSpin({min:500,max:5000,step:100,decimals:0,postfix:'ms'});})();