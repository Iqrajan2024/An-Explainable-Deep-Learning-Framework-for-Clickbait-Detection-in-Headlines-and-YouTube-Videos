var e=class{constructor(e){this.controller=e,this.hoverDelay=500,this.hoverTimer=null,this.currentElement=null,this.initialize()}initialize(){document.addEventListener(`mouseover`,this.onMouseOver.bind(this)),document.addEventListener(`mouseout`,this.onMouseOut.bind(this))}onMouseOver(e){let t=null;t=window.location.hostname.includes(`youtube.com`)?e.target.closest(`a.ytLockupMetadataViewModelTitle`):e.target.closest(`a`),t&&t!==this.currentElement&&(this.currentElement=t,clearTimeout(this.hoverTimer),this.hoverTimer=setTimeout(()=>{this.processHover(t)},this.hoverDelay))}onMouseOut(e){this.currentElement&&e.relatedTarget&&this.currentElement.contains(e.relatedTarget)||(clearTimeout(this.hoverTimer),this.currentElement=null)}processHover(e){if(window.location.hostname.includes(`youtube.com`)){this.controller.handleYoutubeHover(e);return}this.controller.handleArticleHover(e)}isYoutube(e){return e.includes(`youtube.com/watch`)||e.includes(`youtu.be/`)}},t=class{render(e){let t=e.prediction.prediction,n=e.prediction.confidence_percentage,r=e.prediction.badge,i=e.prediction.color;return`

<div class="cd-result-card ${t===`Clickbait`?`danger`:`safe`}">

    <div class="cd-score-circle"
         style="border-color:${i}; color:${i};">

        ${n.toFixed(0)}%

    </div>

    <div class="cd-result-text">

        <div class="cd-prediction-text">

            ${t.toUpperCase()}

        </div>

        <div class="cd-confidence-badge">

            ${r}

        </div>

    </div>

</div>

`}},n=class{constructor(){}render(e){let t=e.explanation||{};return t.positive_words,t.negative_words,`

<div class="cd-summary-card">

    <div class="cd-section-title">

        Key Influential Words

    </div>

    <div class="cd-chip-container">

        ${(t.important_words||[]).map(e=>`

            <span class="cd-chip">

                ${e.word}

            </span>

        `).join(``)}

    </div>

</div>

`}renderWords(e,t){return e.length?e.map(e=>`

    <span class="cd-chip ${t}">

        ${e.word}

    </span>

    `).join(``):`

    <p class="cd-none">

        None

    </p>

    `}},r=class{constructor(){this.confidenceRenderer=new t,this.explanationRenderer=new n}render(e){return`


    <div class="cd-header">

        <div class="cd-title">

            ClickDetect AI

        </div>

        <button
            id="cd-close-btn"
            class="cd-icon-btn">

            ✕

        </button>

    </div>

    <div class="cd-body">

        ${this.confidenceRenderer.render(e)}

        ${this.explanationRenderer.render(e)}

        <div class="cd-footer">

            <button
                id="cd-why-btn"
                class="cd-primary-btn">

                View Full Analysis →

            </button>

        </div>

    </div>


`}},i=class{render(e){let t=(e.explanation||{}).important_words||[];return t.length?`

<div class="cd-importance">

    <h3>

        Feature Importance

    </h3>

    ${t.map(e=>this.renderBar(e)).join(``)}

</div>

`:``}renderBar(e){let t=Math.min(Math.abs(e.importance)*250,100),n=e.direction===`positive`;return`

<div class="cd-bar-item">

    <div class="cd-bar-header">

        <span>

            "${e.word}"

        </span>

        <span>

            ${e.importance>0?`+`:``}
            ${e.importance.toFixed(2)}

        </span>

    </div>

    <div class="cd-bar">

        <div

            class="cd-fill ${n?`positive`:`negative`}"

            style="width:${t}%">

        </div>

    </div>

</div>

`}},a=class{render(e=`ClickDetect AI`){return`

<div class="cd-header">

    <div class="cd-header-left">

        <div class="cd-logo">

            ◎

        </div>

        <div class="cd-title">

            ${e}

        </div>

    </div>

    <button
        class="cd-close"
        title="Close"
    >

        ✕

    </button>

</div>

`}},o=class{constructor(){this.confidenceRenderer=new t,this.visualizationRenderer=new i,this.header=new a}render(e){let t=this.confidenceRenderer.render(e),n=e.explanation?.text?.important_words||[];return`

<div class="cd-popup">

    <div class="cd-header">

        <div class="cd-title">

            ClickDetect AI

        </div>

        <button
            id="cd-close-btn"
            class="cd-icon-btn">

            ✕

        </button>

    </div>

    <div class="cd-body">

        ${t}

        <div class="cd-summary-card">

            <div class="cd-section-title">

                Key Influential Words

            </div>

            <div class="cd-chip-container">

                ${n.length?n.map(e=>`

                        <span class="cd-chip">

                            ${e.word}

                        </span>

                    `).join(``):`<span class="cd-none">None</span>`}

            </div>

        </div>


        <div class="cd-footer">

            <button
                id="cd-why-btn"
                class="cd-primary-btn">

                View Full Analysis →

            </button>

        </div>

    </div>

</div>

`}},s=class{constructor(){}render(e){let t=e.explanation||{},n=e.headline||``,r=t.summary||`No explanation available.`,i=t.important_words||[];return e.prediction?.label||e.label,e.confidence_percentage??e.confidence,e.confidence_level,`

    <div class="cd-header">

        <button
            id="cd-back-btn"
            class="cd-icon-btn">

            ←

        </button>

        <div class="cd-title">

            Detailed Analysis

        </div>

        <button
            id="cd-close-btn"
            class="cd-icon-btn">

            ✕

        </button>

    </div>

    <div class="cd-body">

        ${this.renderHeadline(n)}

        ${this.renderSummary(r)}


        ${this.renderImportance(i)}

        <div class="cd-footer-note">

            Words importance shows which words had
            the greatest influence on the AI prediction.

        </div>

    </div>

    `}renderHeadline(e){return`

    <div class="cd-card">

        <h3>

            Headline

        </h3>

        <p class="cd-headline">

            ${e}

        </p>

    </div>

    `}renderSummary(e){return`

    <div class="cd-card">

        <h3>

            AI Reasoning

        </h3>

        <p class="cd-summary">

            ${e}

        </p>

    </div>

    `}renderImportance(e){return e.length?`

<div class="cd-card">

    <h3>

        Most Influential Words Importance

    </h3>

    <div class="cd-legend">

    <div class="cd-legend-item">

        <span class="cd-legend-color increase"></span>

        Increases Clickbait Score

    </div>

    <div class="cd-legend-item">

        <span class="cd-legend-color decrease"></span>

        Reduces Clickbait Score

    </div>

</div>


    ${e.map(e=>`

    <div class="cd-feature">

        <div class="cd-feature-top">

            <span>

                ${e.word}

            </span>

            <span>

                ${Math.abs(e.importance).toFixed(3)}

            </span>

        </div>

        <div class="cd-bar">

            <div
                class="cd-bar-fill ${e.direction}"
                style="width:${Math.min(Math.abs(e.importance)*400,100)}%">

            </div>

        </div>

    </div>

    `).join(``)}

</div>

`:`

<div class="cd-card">

    <h3>

         Most Influential Words Importance

    </h3>

    <div class="cd-empty">

        No influential words available.

    </div>

</div>

`}},c=class{constructor(){}render(e){let t=e.explanation||{},n=t.summary||`No explanation available.`,r=e.title||``,i=t.text?.important_words||[];return t.text?.positive_words,t.text?.negative_words,`


<div class="cd-popup">

<div class="cd-header">

    <button
        id="cd-back-btn"
        class="cd-icon-btn">

        ←

    </button>

    <div class="cd-title">

        Analysis Explanation

    </div>

    <button
        id="cd-close-btn"
        class="cd-icon-btn">

        ✕

    </button>

</div>



<div class="cd-body">

    <div class="cd-card">

        <h3>

            Video Title

        </h3>

        <p class="cd-headline">

            ${r}

        </p>

    </div>

    <div class="cd-card">

        <h3>

            AI Reasoning

        </h3>

        <p class="cd-summary">

            ${n}

        </p>

    </div>


    ${this.renderImportance(i)}

    <div class="cd-footer">

        <button
            id="cd-metadata-btn"
            class="cd-primary-btn">

            View Metadata Analysis →

        </button>

    </div>

</div>

</div>

`}renderImportance(e){return e.length?`

<div class="cd-card">

    <h3>

        Most Influential Text Words

    </h3>

    <div class="cd-legend">

        <div class="cd-legend-item">

            <span class="cd-legend-color increase"></span>

            Increases Clickbait Score

        </div>

        <div class="cd-legend-item">

            <span class="cd-legend-color decrease"></span>

            Reduces Clickbait Score

        </div>

    </div>

    ${e.map(e=>`

<div class="cd-feature">

    <div class="cd-feature-top">

        <span>

            ${e.word}

        </span>

        <span>

            ${Math.abs(e.importance).toFixed(3)}

        </span>

    </div>

    <div class="cd-bar">

        <div
            class="cd-bar-fill ${e.direction}"
            style="width:${Math.min(Math.abs(e.importance)*400,100)}%">

        </div>

    </div>

</div>

`).join(``)}

</div>

`:`

<div class="cd-card">

    <h3>

        Most Influential Text Words

    </h3>

    <div class="cd-empty">

        No influential words available.

    </div>

</div>

`}},l=class{constructor(){}render(e){let t=e.explanation?.metadata||{},n=t.summary||`No metadata explanation available.`,r=t.important_features||[],i=t.positive_features||[],a=t.negative_features||[];return`

<div class = "cd-popup">

<div class="cd-header">

    <button
        id="cd-metadata-back-btn"
        class="cd-icon-btn">

        ←

    </button>

    <div class="cd-title">

        Metadata Analysis

    </div>

    <button
        id="cd-close-btn"
        class="cd-icon-btn">

        ✕

    </button>

</div>



<div class="cd-body">

    <div class="cd-card">

        <h3>

            AI Reasoning

        </h3>

        <p class="cd-summary">

            ${n}

        </p>

    </div>

    ${this.renderImportance(r,i,a)}



</div>
</div>

`}renderImportance(e,t,n){return e.length?`

<div class="cd-card">

    <h3>

        Most Influential Metadata Features

    </h3>

    <div class="cd-legend">

        <div class="cd-legend-item">

            <span class="cd-legend-color increase"></span>

            Increases Clickbait Score

        </div>

        <div class="cd-legend-item">

            <span class="cd-legend-color decrease"></span>

            Reduces Clickbait Score

        </div>

    </div>

    ${e.map(e=>`

<div class="cd-feature">

    <div class="cd-feature-top">

        <span>

            ${e.feature}

        </span>

        <span>

            ${Math.abs(e.impact).toFixed(3)}

        </span>

    </div>

    <div class="cd-bar">

        <div
            class="cd-bar-fill ${e.direction}"
            style="width:${Math.min(Math.abs(e.impact)*3e3,100)}%">

        </div>

    </div>

</div>

`).join(``)}

</div>

`:`

<div class="cd-card">

    <h3>

        Most Influential Metadata Features

    </h3>

    <div class="cd-empty">

        No metadata available.

    </div>

</div>

`}},u=class{constructor(){this.popup=null,this.articleRenderer=new r,this.youtubeRenderer=new o,this.youtubeExplanationRenderer=new c,this.youtubeMetadataRenderer=new l,this.explanationPageRenderer=new s,this.lastElement=null,this.lastResponse=null,this.lastType=null,this.createPopup(),this.registerEvents(),this.originalResponse=null}createPopup(){this.popup=document.createElement(`div`),this.popup.id=`clickdetect-popup`,this.popup.className=`cd-popup-container`,this.popup.style.display=`none`,document.body.appendChild(this.popup)}registerEvents(){document.addEventListener(`mousedown`,e=>{this.popup.style.display===`block`&&!this.popup.contains(e.target)&&this.hide()}),document.addEventListener(`keydown`,e=>{e.key===`Escape`&&this.hide()})}showArticle(e,t){this.popup.style.width=`340px`,this.popup.style.maxWidth=`340px`,this.popup.style.height=`420px`,this.lastElement=e,this.lastResponse=t,this.originalResponse=t,this.lastType=`article`,this.positionPopup(e),this.popup.innerHTML=this.articleRenderer.render(t),this.attachEvents(),this.show()}showYoutube(e,t){this.popup.style.width=`340px`,this.popup.style.maxWidth=`340px`,this.popup.style.height=`420px`,this.lastElement=e,this.lastResponse=t,this.originalResponse=t,this.lastType=`youtube`,this.positionPopup(e),this.popup.innerHTML=this.youtubeRenderer.render(t),this.attachEvents(),this.show()}showYoutubeExplanation(){this.popup.style.width=`340px`,this.popup.style.maxWidth=`340px`,this.popup.style.height=`420px`,this.popup.innerHTML=this.youtubeExplanationRenderer.render(this.lastResponse),this.attachEvents()}showMetadataAnalysis(){this.popup.style.width=`340px`,this.popup.style.maxWidth=`340px`,this.popup.style.height=`420px`,this.popup.innerHTML=this.youtubeMetadataRenderer.render(this.lastResponse),this.attachEvents()}showLoading(){this.popup.style.width=`220px`,this.popup.style.maxWidth=`220px`,this.popup.style.height=`60px`,this.positionPopup(),this.popup.innerHTML=`
        <div class="cd-loading-toast">

            <div class="cd-spinner"></div>

            <div class="cd-loading-text">
                Analyzing...
            </div>

        </div>
    `,this.show()}showExplanation(){this.popup.style.width=`340px`,this.popup.style.maxWidth=`340px`,this.popup.style.height=`420px`,this.popup.innerHTML=this.explanationPageRenderer.render(this.lastResponse),this.attachEvents()}attachEvents(){let e=this.popup.querySelector(`#cd-close-btn`);e&&(e.onclick=()=>{this.hide()});let t=this.popup.querySelector(`#cd-why-btn`);t&&(t.onclick=()=>{console.log(`WHY BUTTON CLICKED`),console.log(`lastType =`,this.lastType),this.lastType==`article`?this.showExplanation():(console.log(`Opening YouTube explanation`),this.showYoutubeExplanation())});let n=this.popup.querySelector(`#cd-metadata-btn`);n&&(n.onclick=()=>{this.showMetadataAnalysis()});let r=this.popup.querySelector(`#cd-metadata-back-btn`);r&&(r.onclick=()=>{this.showYoutubeExplanation()});let i=this.popup.querySelector(`#cd-back-btn`);i&&(i.onclick=()=>{this.lastType===`article`?this.showArticle(this.lastElement,this.lastResponse):this.showYoutube(this.lastElement,this.originalResponse)})}showError(e,t){this.positionPopup(e),this.popup.innerHTML=`

<div class="cd-error-toast">

    <div class="cd-error-icon">

        <img
            src="${chrome.runtime.getURL(`icons/alert-triangle.svg`)}"
            alt="Warning"
        >

    </div>

    <div class="cd-error-text">

        Unable to connect to backend

    </div>

</div>
`,this.attachEvents(),this.show()}positionPopup(){this.popup.style.position=`fixed`,this.popup.style.right=`20px`,this.popup.style.bottom=`20px`,this.popup.style.left=`auto`,this.popup.style.top=`auto`,this.popup.style.zIndex=`999999`}show(){this.popup.style.display=`block`,requestAnimationFrame(()=>{this.popup.classList.add(`show`)})}hide(){this.popup.classList.remove(`show`),setTimeout(()=>{this.popup.style.display=`none`},180)}},d=class{constructor(){this.previousElement=null,this.originalStyle={}}highlight(e,t){e&&(this.clear(),this.previousElement=e,this.originalStyle={outline:e.style.outline,background:e.style.backgroundColor,transition:e.style.transition},e.style.transition=`all 0.2s ease`,e.style.outline=`2px solid ${t}`,e.style.backgroundColor=`${t}20`)}clear(){this.previousElement&&(this.previousElement.style.outline=this.originalStyle.outline,this.previousElement.style.backgroundColor=this.originalStyle.background,this.previousElement.style.transition=this.originalStyle.transition,this.previousElement=null,this.originalStyle={})}},f=class{constructor(){}extract(e){if(!e)return null;let t=this.extractHeadline(e);if(!t)return null;let n=e.href||``,r=``;try{r=new URL(n).hostname}catch{r=``}return{headline:t,url:n,domain:r}}extractHeadline(e){let t=e.innerText||e.textContent||``;return t=t.trim(),t.length===0?null:t}},p=class{constructor(){}extract(e){if(!e)return null;let t=e.closest(`ytd-rich-item-renderer, ytd-video-renderer, ytd-compact-video-renderer, yt-lockup-view-model`);if(!t)return null;let n=e,r={videoId:this.extractVideoId(n),title:this.extractTitle(n),channel_title:this.extractChannel(t),thumbnail:this.extractThumbnail(t),titleElement:n};return console.log(`VIDEO EXTRACTED`,r),r}extractVideoId(e){try{return new URL(e.href).searchParams.get(`v`)||``}catch{return``}}extractTitle(e){return(e.getAttribute(`aria-label`)||e.textContent||``).trim()}extractChannel(e){let t=e.querySelectorAll(`a`);for(let e of t)if(!e.classList.contains(`ytLockupMetadataViewModelTitle`))return e.textContent.trim();return``}extractThumbnail(e){let t=e.querySelector(`img`);return t?.currentSrc||t?.src||``}},m=class{constructor(){this.BASE_URL=`http://127.0.0.1:8000`}async post(e,t){try{let n=await fetch(`${this.BASE_URL}${e}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!n.ok)throw Error(`Backend Error ${n.status}`);return await n.json()}catch(e){return console.error(`API Error`,e),null}}async predictHeadline(e){return await this.post(`/predict/headline`,{headline:e.headline})}async predictYoutube(e){return await this.post(`/predict/youtube`,{videoId:e.videoId})}};new class{constructor(){this.articleService=new f,this.youtubeService=new p,this.api=new m,this.popup=new u,this.highlighter=new d,this.detector=new e(this),this.cache=new Map,console.log(`ClickDetect AI initialized.`)}async handleArticleHover(e){try{let t=this.articleService.extract(e);if(!t)return;let n=t.url;if(this.cache.has(n)){let t=this.cache.get(n);this.popup.showArticle(e,t),this.highlighter.highlight(e,t.color);return}this.popup.showLoading(e);let r=await this.api.predictHeadline(t);if(console.log(`ARTICLE RESPONSE`),console.log(r),!r){this.popup.showError(e,`Unable to contact backend.`);return}let i={...r,headline:t.headline,url:t.url,domain:t.domain};this.cache.set(n,i),this.popup.showArticle(e,i),this.highlighter.highlight(e,r.prediction.color)}catch(e){console.error(e)}}async handleYoutubeHover(e){console.log(`HANDLE YOUTUBE HOVER`);try{let t=this.youtubeService.extract(e);if(!t)return;let n=t.videoId;if(this.cache.has(n)){let t=this.cache.get(n);this.popup.showYoutube(e,t),this.highlighter.highlight(e,t.color);return}this.popup.showLoading(e);let r=await this.api.predictYoutube(t);if(console.log(`VIDEO EXTRACTED`),console.log(t),console.log(`BACKEND RESPONSE:`,r),console.log(`JSON:`,JSON.stringify(r,null,2)),!r){this.popup.showError(e,`Unable to contact backend.`);return}let i={...r,title:r.title,thumbnail:r.thumbnail,channel_title:r.channel_title,videoId:t.videoId};this.cache.set(n,i),this.popup.showYoutube(t.titleElement,i),this.highlighter.highlight(t.titleElement,r.prediction.color)}catch(e){console.error(`YOUTUBE ERROR`),console.error(e),console.error(e.stack)}}};