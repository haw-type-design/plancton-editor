
% rebase('templates/base.tpl')
<section id="" class="index" >
    <nav>
        <div class="header">
            <a href="/" class="main-logo"><h1>P L A N C T O N</h1></a>
            <hr>
        </div>
    </nav>

    <div class="project-index">
        <p>Plancton is a development environment for making digital typography. It’s built on <a href="https://www.tug.org/docs/metapost/mpman.pdf" target="_blank">Metapost</a></p>

        <p>Projects:</p>
        <div id='projects' class='projects-grid'>
            % for project in projectsjson:
            <a class= 'grid-item' href="/type/{{ project['font-id'] }}">{{ project['font-name'] }}</a>

            % end

            <div class="new-project">
                <input class="grid-item" id="new-project" placeholder="+ New Project">
                <a id="add-project">Create new project</a>
            </div>

        </div>


        <p>Documentation <a href="https://github.com/simonthi/plancton-editor/" target="_blank">here</a></p>
    </div>
    <script>
        document.getElementById("add-project").addEventListener("click", function(){
            window.location = "/create/" + document.getElementById('new-project').value.replace(" ", "-");
        });
    </script>

</section>
