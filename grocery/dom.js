const { document, trustedTypes, DOMParser, XMLSerializer } = window;
const symbol = Symbol('source');
const [source, template, render] = [symbol, (source, { ...data } = {}) => ({[symbol]: source, ...data}), renderer(context)];
const context = {
    document,
    parser: new DOMParser(),
    policy: trustedTypes?.createPolicy('dom-engine', {
        createHTML: source => source
    }),
    serializer: new XMLSerializer(),
    source
}

const fragments = new Map();

const symbols = {doctype: Symbol('doctype'), node: Symbol('node'), map: Symbol('map')};

const parts = /(^\s*<!doctype [^>]+>|)([\s\S]*)$/i
const identifier = /{((\??)([a-z]\w*(?:\.[a-z]\w*)*))}/g
const attribute = /(<!--dom-engine::(\??)([a-z]\w*(?:\.[a-z]\w*)*)::dom-engine-->)/g
const text = /^(dom-engine::(\??)([a-z]\w*(?:\.[a-z]\w*)*)::dom-engine)$/g
const escaped = /^(&lt;!--dom-engine::(\??)([a-z]\w*(?:\.[a-z]\w*)*)::dom-engine--&gt;)/g

const token = ([, identifier, optional, key]) => ({identifier, key, optional: optional === '?'})

const [
    html, 
    mark, 
    identify,
    search
] = [
    source=>context.policy?.createHTML(source) ?? source,
    source=>source.replace(identifier, '<!--dom-engine::$1::dom-engine-->'),
    (pattern, value)=>[...value.matchAll(pattern)].map(token),
    node=>{
        const { ownerDocument } = node;
        let [nodes, iterator, current] = [[], ownerDocument.createNodeIterator(node, 129), null]
        while(current = iterator.nextNode()){
            nodes.push(current)
        }
        return nodes
    }
];

const tokenize=node=>{
    const map = new Map();
    for(const [key, current] of search(node).entries()){
        const {nodeName} = current;
        if(nodeName === 'TITLE'){
            const tokens = identify(escaped, current.innerHTML);
            if(tokens.length){map.set(key, {tokens})}
        }else if(nodeName === 'SCRIPT'){
            const tokens = identify(attribute, current.textContent);
            if(tokens.length){map.set(key, {tokens})}
        }else if(nodeName === 'TEXTAREA'){
            const tokens = identify(attribute, current.value);
            if(tokens.length){map.set(key, {tokens})}
        }else if(current.nodeType === 1){
            const attributes = new Map();
            for(const {name, value} of current.attributes){
                const tokens = identify(attribute, value);
                if(tokens.length){attributes.set(name, tokens)}
            }
            if(attributes.size){map.set(key, {attributes})}
        }else{
            const tokens = identify(text, current.nodeValue);
            if(tokens.length){map.set(key, {tokens})}
        }
    }
    return map;
}

const fragment=source=>{
    const {document} = context;
    const template = document.createElement('template');
    template.innerHTML = html(mark(source));
    return {[context.source]: source, [symbols.doctype]: '', [symbols.node]: template.content, [symbols.map]: tokenize(template.content)}
}

function clone(template, parse){
    const {[context.source]: source} = template;
    if(!fragments.has(source)){fragments.set(source, parse(source))}
    const fragment = fragments.get(source);
    return {...template, ...fragment, [symbols.node]: fragment[symbols.node].cloneNode(true)}
}

const isFilled = (value = null) => value !== null

function value(tokens, node, name, template){
    const {length} = tokens;
    if(!length){return}
    const initial = node.getAttribute(name);
    let value = initial;
    for(const {identifier, key, optional} of tokens){
        const [parts, resolved] = [value.split(identifier), resolve(key, optional, template)];
        value = parts.join(resolved || '');
    }
    if(length === 1 && value === '' && initial === tokens[0].identifier){
        node.removeAttribute(name)
    }else{
        node.setAttribute(name, value);
    }
}

function fill(template){
    const {[symbols.node]: node, [symbols.map]: map} = template;
    const nodes = search(node);
    for(const [key, {attributes, tokens}] of map){
        const node = nodes[key];
        if(attributes){
            for(let [name, tokens] of attributes){
                value(tokens, node, name, template);
            }
        }else if(tokens){
            content(tokens, node, template);
        }
    }
    return node
}

function content(tokens, node, template){
    let [target, content, asValue, nodes] = [...pick(node), []];
    for(const {identifier, key, optional} of tokens){
        const [[prefix], value] = [content.split(identifier), pick(node)];
        const replacements = Array.isArray(value) ? value : value && typeof value === 'object' && value[Symbol.iterator] ? [...new Map(value).values()] : [value];
        nodes.push(prefix, ...replacements.filter(isFilled).map(child));
        content = content.replace(`${prefix}${identifier}`, '');
    }
    if(asValue){
        target.textContent = nodes.join('');
    }else{
        target.replaceWith(...nodes, content);
    }
}

function pick(node){
    const {nodeName} = node;
    if(nodeName === 'TITLE'){
        return [node.firstChild, node.innerHTML];
    }else if(nodeName === 'SCRIPT'){
        return [node.firstChild, node.textContent];
    }else if(nodeName === 'TEXTAREA'){
        return [node, node.value, true];
    }
    return [node, node.nodeValue]
}

function child (value) {return value?.[context.source] ? fill(clone(value, fragment)) : value}

function resolve(key, optional, template){
    const source = template[context.source];
    return key.split('.').reduce((data, name)=>{
        const {[name]: value = null} = data ?? {};
        if(value === null && !optional){throw new Error(`Missing ${key} in \`${source}\``)}
        return value
    }, template);
}

function renderer({document, parser, policy, source}){
    if(!context){context = {document, parser, policy, source}}
    return template=>{
        const cloned = clone(template, source=>{
            const [{parser}, [,doctype]] = [context, source.match(parts)];
            if(!doctype){return fragment(source)}
            const node = parser.parseFromString(html(mark(source)), 'text/html').documentElement;
            return {[context.source]: source, [symbols.doctype]: doctype, [symbols.node]: node, [symbols.map]: tokenize(node)}
        })
        const {[symbols.node]: node} = cloned; fill(cloned);
        return node;
    }
}