import React from 'react';
import Remarkable from 'remarkable';
import {Link} from 'react-router-dom';
import hljs from 'highlightjs'
import styled from 'styled-components'

//var md = new Remarkable();layout.html
// Actual default values

var md = new Remarkable('full', {
  html:         false,        // Enable HTML tags in source
  xhtmlOut:     false,        // Use '/' to close single tags (<br />)
  breaks:       true,        // Convert '\n' in paragraphs into <br>
  langPrefix:   'language-',  // CSS language prefix for fenced blocks
  linkify:      true,         // autoconvert URL-like texts to links
  linkTarget:   '',           // set target to open link in

  // Enable some language-neutral replacements + quotes beautification
  typographer:  false,

  // Double + single quotes replacement pairs, when typographer enabled,
  // and smartquotes on. Set doubles to '«»' for Russian, '„“' for German.
  quotes: '“”‘’',

  // Highlighter function. Should return escaped HTML,
  // or '' if input not changed
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(lang, str).value;
      } catch (__) {}
    }

    try {
      return hljs.highlightAuto(str).value;
    } catch (__) {}

    return ''; // use external default escaping
  }
});




class Store {
    
    constructor(config){
        // var indexer = config.indexer 
        // var url = config.url 
        // this.data = {}
        
        // that =this; 

        // fetch(url).then(function(response)
        //     {
        //         return response.json();
        //     }).then(function(json){
        //         console.log(json);
        //         that.data[ indexer(json) ] = json
        //     });
    }

    update(indexer,url,onSuccess){
        
        this.data = {}
        
        var that =this; 

        fetch(url).then(function(response)
            {
                return response.json();
            }).then(function(json){
                //that.data[  ] = json
                indexer(that.data, json)

                if (onSuccess != undefined){
                    onSuccess(json)
                }
            });

    }

    get(k){
        return this.data[k];
    }

}



function loadApplicationContext(that){
    var props = that.props; 
    if (props.context == undefined) {
        console.log("application-context-unset!");
        console.log(props);
    }else{
        console.log("application-context-set!");
        console.log(props.context);
        
    }

}

function getApplicatioContext(that){
    var props =that.props; 
    if (props.context == undefined) {
        return null; 
    }
    
    return that.props.context; 
}

class Index extends  React.Component{
    constructor(props){
        super(props);
        this.state = {};
        console.log("index-loaded");
        loadApplicationContext(this);
    }

    render() {

       return  ( <PageLayout> 
                    <PageContent>
                        <h1> Posts </h1>
                        <Toc index="/content/index.json"/>
                </PageContent>
           
           </PageLayout>);
    }



    componentDidMount(){
            console.log("Index mounted");

    }

}

const Card=styled.div`


`
class Toc extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            index: null 
        };
    }

    componentDidMount(){
            var url = this.props.index;
            var that = this; 
            fetch(url).then(function(response)
            {
                return response.json();
            }).then(function(json){
                console.log(json);
                that.setState({index: json});
            });

    }
    render(){
        
        var contents = <div /> ;
        if (this.state.index != null){
                contents  = this.state.index.map(
                    (entry) => {
                        return (<Card> 
                                    <PageSummary title={entry.title} date={entry.date} file={entry.file} meta={entry}/>
                                </Card>)
                    }
                );
        }
        
        return (<div> 
               {contents}
               
            </div>);
    }
}

function parse(mdFile){
    var meta = /---/
    if(mdFile.match(meta) == null) {
        return {"content":mdFile, "title":"titled", "date":"__undef__"};
    }
    console.log("parsing ... " + mdFile);
    var segments = mdFile.split(/---\s*\n/);
    var content = null;
    var meta = {title: null }; 

    if(segments.length==1){
        content = segments[0];
    }else{
        var lines = segments[0].split("\n").map( (line) => {
                var kvpair = line.split(":");
                var k = kvpair[0];
                var v = kvpair[1];
                meta[k] = v; 
        });
        content = segments[1];
    }
    console.log(meta);
    return {"content":content, "title":meta.title, "date":"__undef__", "meta": meta};

}

function getContent(article){
    if (article==null){
        return "__undef__";
    }
    return article.content; 


}

const Row = styled.div`
    display: flex;
    & > div {
        padding-right: 1em;        
        //background: #929fad;
         width:auto;
         align-self: center;

     
       }
     
       & > div:nth-child(odd){
        padding-right: 1em;
        align-self: center;

        //background: #e3e7ea;
         width:auto;
       }
`
class PageSummary extends React.Component{
    render(){
        console.log(this.props.file);
        function assetLinks(meta){
            
            if (meta.assets != ""){
                return (<div><a href="/assets"> <i class="fa fa-files-o fa-1x">  </i> </a></div>) 
            }
            return (<div></div>) 
            
        }

        var assets = assetLinks(this.props.meta);
        return (
            <div> 
                <Row>  
                    <div> <h3>{this.props.title}  </h3> </div>  
                    {assets}    
                </Row>
                {/* <div> {this.props.date} </div> */ } 
                <div>{this.props.meta.preview}</div>
                
                <div> <h4> <Link to={"/page/" + this.props.file}  meta={this.props.meta}> Read More </Link> </h4>  </div> 
                
                
            </div>
        );
    }    
}

//<div dangerouslySetInnerHTML={{ __html: md.render("# I fugging rule biyeeeetch!") }} />
const PageLayout = styled.div`

        display: grid; 
        /*grid-template-columns: 1fr  1fr 1fr ;*/
        grid-template-columns: 1fr  minmax(auto,50em) 1fr ;
        grid-auto-columns: minmax(100px,auto);
        grid-column-gap:  1em;
        grid-row-gap: 1em;
        //padding: 0 20px;


    & > div {
       // background: #929fad;
        width:auto;
        //padding: 1em;

    
      }
    
      & > div:nth-child(odd){
       // background: #e3e7ea;
        width:auto;
      }
    

    `;

const PageHeading = styled.div ` 
    grid-column: 1/4;
`;

const PageContent = styled.div `
      grid-column: 2/3;
`; 
class Page extends React.Component {

    constructor(props){
        
        super(props);
        console.log("page-loaded");
        loadApplicationContext(this);

        var k = "page-"+this.props.match.params.name;
        this.state = {
            article:null,
       
        
        };


        //this.setState("meta",getApplicatioContext(this)[k]);
        
        console.log("key:",k)
        console.log(getApplicatioContext(this));
        console.log(getApplicatioContext(this).store.get(k));
        
        
    }

    

    componentDidMount(){
            //console.log(this.props);
            var mdUrl = "/content/" + this.props.match.params.name + ".md";
            var that = this; 
            fetch(mdUrl).then(function(response)
            {
                return response.text();
            }).then(function(text){
                that.setState({article: parse(text)});
            });


    }

    getPageMeta(){
        
        return getApplicatioContext(this).store.get("page-"+this.props.match.params.name);
    }
    render (){
      
        return (
            <PageLayout><Link to="/">Go Home Again:  </Link>
                <PageHeading><center><h1>  {this.getPageMeta()["title"]} </h1></center></PageHeading>
                <div/>
                <PageContent dangerouslySetInnerHTML={{ __html:md.render(getContent(this.state.article))  }}/>
                <div/>
                
            </PageLayout>
        );
    }
}
/*
    <div dangerouslySetInnerHTML={{ __html: md.render(this.props.file) }} />
                        <a href={"content/" + this.props.file}> {this.props.title}</a>  

                <div> A one way ticket </div> 
                   <div> Content:  
                            {getContent(this.state.article)}
                    </div>*/

export  {Index, Page,Store}; 
/*ReactDOM.render(
  <h1>Hello, world!</h1>,
  document.getElementById('root')
);*/