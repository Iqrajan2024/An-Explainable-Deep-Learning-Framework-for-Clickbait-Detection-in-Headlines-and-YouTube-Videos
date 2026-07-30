var e=class{constructor(e){this.controller=e,this.hoverDelay=500,this.hoverTimer=null,this.currentElement=null,this.initialize()}initialize(){document.addEventListener(`mouseover`,this.onMouseOver.bind(this)),document.addEventListener(`mouseout`,this.onMouseOut.bind(this))}onMouseOver(e){let t=e.target.closest(`a`);t&&t!==this.currentElement&&(this.currentElement=t,clearTimeout(this.hoverTimer),this.hoverTimer=setTimeout(()=>{this.processHover(t)},this.hoverDelay))}onMouseOut(){clearTimeout(this.hoverTimer)}processHover(e){let t=e.href||``;if(this.isYoutube(t)){this.controller.handleYoutubeHover(e);return}this.controller.handleArticleHover(e)}isYoutube(e){return e.includes(`youtube.com/watch`)||e.includes(`youtu.be/`)}},t=class{constructor(){}render(e){let t=e.prediction||`Unknown`,n=Number(e.confidence||0).toFixed(1),r=e.color||`#999999`;return`

<div class="cd-confidence-card">

    <div class="cd-prediction">

        <span class="cd-label">

            Prediction

        </span>

        <span
            class="cd-value"
            style="color:${r};"
        >

            ${t}

        </span>

    </div>

    <div class="cd-confidence">

        <span class="cd-label">

            Confidence

        </span>

        <span class="cd-value">

            ${n}%

        </span>

    </div>

    <div class="cd-progress">

        <div
            class="cd-progress-fill"
            style="
                width:${n}%;
                background:${r};
            ">
        </div>

    </div>

</div>

`}},n=class{constructor(){}render(e){let t=e.reason||`No explanation available.`,n=e.positive_words||[],r=e.negative_words||[];return`

<div class="cd-explanation">

    <h3>Why?</h3>

    <p>

        ${t}

    </p>

    ${this.renderWords(`Positive Indicators`,n,`positive`)}

    ${this.renderWords(`Negative Indicators`,r,`negative`)}

</div>

`}renderWords(e,t,n){return t.length?`

<div class="cd-word-group">

    <h4>${e}</h4>

    <div class="cd-chip-container">

        ${t.map(e=>`<span class="cd-chip ${n}">
                ${e}
            </span>`).join(``)}

    </div>

</div>

`:``}},r=class{constructor(){this.confidenceRenderer=new t,this.explanationRenderer=new n}render(e){return`

<div class="cd-popup">

    <div class="cd-header">

        <h2>ClickDetect AI</h2>

    </div>

    <div class="cd-body">

        ${this.confidenceRenderer.render(e)}

        ${this.explanationRenderer.render(e)}

    </div>

</div>

`}},i=class{constructor(){}render(e){let t=e.gradcam||null,n=e.image_reason||`No image explanation available.`,r=e.metadata_reason||[];return`

<div class="cd-visualization">

    <h3>Visual Analysis</h3>

    ${this.renderGradCAM(t)}

    <div class="cd-image-reason">

        <p>${n}</p>

    </div>

    ${this.renderMetadata(r)}

</div>

`}renderGradCAM(e){return e?`

<div class="cd-gradcam">

    <img
        src="data:image/png;base64,${e}"
        alt="Grad-CAM Heatmap"
    >

</div>

`:``}renderMetadata(e){return e.length?`

<div class="cd-metadata">

    <h4>Metadata Indicators</h4>

    <ul>

        ${e.map(e=>`<li>${e}</li>`).join(``)}

    </ul>

</div>

`:``}},a=class{constructor(){this.confidenceRenderer=new t,this.explanationRenderer=new n,this.visualizationRenderer=new i}render(e){return`

<div class="cd-popup">

    <div class="cd-header">

        <h2>ClickDetect AI</h2>

    </div>

    <div class="cd-body">

        ${this.confidenceRenderer.render(e)}

        ${this.explanationRenderer.render(e)}

        ${this.visualizationRenderer.render(e)}

    </div>

</div>

`}},o=class{constructor(){this.popup=null,this.createPopup(),this.articleRenderer=new r,this.youtubeRenderer=new a}createPopup(){this.popup=document.createElement(`div`),this.popup.id=`clickdetect-popup`,this.popup.style.display=`none`,document.body.appendChild(this.popup)}showArticle(e,t){this.positionPopup(e),this.popup.innerHTML=this.articleRenderer.render(t),this.popup.style.display=`block`}showYoutube(e,t){this.positionPopup(e),this.popup.innerHTML=this.youtubeRenderer.render(t),this.popup.style.display=`block`}hide(){this.popup.style.display=`none`}positionPopup(e){let t=e.getBoundingClientRect();this.popup.style.position=`fixed`,this.popup.style.top=`${t.bottom+10}px`,this.popup.style.left=`${t.left}px`}showLoading(e){this.positionPopup(e),this.popup.innerHTML=`

            <div class="cd-loading">

                Analyzing...

            </div>

        `,this.popup.style.display=`block`}showError(e,t){this.positionPopup(e),this.popup.innerHTML=`

            <div class="cd-error">

                ${t}

            </div>

        `,this.popup.style.display=`block`}},s=class{constructor(){this.previousElement=null,this.originalStyle={}}highlight(e,t){e&&(this.clear(),this.previousElement=e,this.originalStyle={outline:e.style.outline,background:e.style.backgroundColor,transition:e.style.transition},e.style.transition=`all 0.2s ease`,e.style.outline=`2px solid ${t}`,e.style.backgroundColor=`${t}20`)}clear(){this.previousElement&&(this.previousElement.style.outline=this.originalStyle.outline,this.previousElement.style.backgroundColor=this.originalStyle.background,this.previousElement.style.transition=this.originalStyle.transition,this.previousElement=null,this.originalStyle={})}},c=class{constructor(){}extract(e){if(!e)return null;let t=this.extractHeadline(e);if(!t)return null;let n=e.href||``,r=``;try{r=new URL(n).hostname}catch{r=``}return{headline:t,url:n,domain:r}}extractHeadline(e){let t=e.innerText||e.textContent||``;return t=t.trim(),t.length===0?null:t}},l=class{constructor(){}extract(e){return e?{videoId:this.extractVideoId(e),title:this.extractTitle(e),channel_title:this.extractChannel(e),thumbnail:this.extractThumbnail(e)}:null}extractVideoId(e){let t=e.closest(`a`);if(!t)return``;try{return new URL(t.href).searchParams.get(`v`)||``}catch{return``}}extractTitle(e){return(e.innerText||e.textContent||``).trim()}extractChannel(e){let t=document.querySelector(`#channel-name`);return t?t.innerText.trim():``}extractThumbnail(e){let t=e.closest(`ytd-rich-item-renderer`)?.querySelector(`img`);return t?t.currentSrc||t.src:``}},u=class{constructor(){this.BASE_URL=`http://127.0.0.1:8000`}async post(e,t){try{let n=await fetch(`${this.BASE_URL}${e}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!n.ok)throw Error(`Backend Error ${n.status}`);return await n.json()}catch(e){return console.error(`API Error`,e),null}}async predictHeadline(e){return await this.post(`/predict/headline`,{headline:e.headline})}async predictYoutube(e){return await this.post(`/predict/youtube`,{videoId:e.videoId})}};new class{constructor(){this.articleService=new c,this.youtubeService=new l,this.api=new u,this.popup=new o,this.highlighter=new s,this.detector=new e(this),this.cache=new Map,console.log(`ClickDetect AI initialized.`)}async handleArticleHover(e){try{let t=this.articleService.extract(e);if(!t)return;let n=t.url;if(this.cache.has(n)){let t=this.cache.get(n);this.popup.showArticle(e,t),this.highlighter.highlight(e,t.color);return}this.popup.showLoading(e);let r=await this.api.predictHeadline(t);if(!r){this.popup.showError(e,`Unable to contact backend.`);return}this.cache.set(n,r),this.popup.showArticle(e,r),this.highlighter.highlight(e,r.color)}catch(e){console.error(e)}}async handleYoutubeHover(e){try{let t=this.youtubeService.extract(e);if(!t)return;let n=t.videoId;if(this.cache.has(n)){let t=this.cache.get(n);this.popup.showYoutube(e,t),this.highlighter.highlight(e,t.color);return}this.popup.showLoading(e);let r=await this.api.predictYoutube(t);if(!r){this.popup.showError(e,`Unable to contact backend.`);return}this.cache.set(n,r),this.popup.showYoutube(e,r),this.highlighter.highlight(e,r.color)}catch(e){console.error(e)}}};