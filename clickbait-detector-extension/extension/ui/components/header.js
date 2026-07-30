/*
===========================================================
ClickDetect AI

Header Component
===========================================================
*/

export class Header {

    render(title = "ClickDetect AI") {

        return `

<div class="cd-header">

    <div class="cd-header-left">

        <div class="cd-logo">

            ◎

        </div>

        <div class="cd-title">

            ${title}

        </div>

    </div>

    <button
        class="cd-close"
        title="Close"
    >

        ✕

    </button>

</div>

`;

    }

}