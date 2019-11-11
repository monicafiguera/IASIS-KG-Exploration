/* global Promise, fetch, window, cytoscape, document, tippy, _ */

Promise.all([
    fetch('/static/js/libs/cy-style.json')
        .then(function(res) {
            return res.json();
        }),
    fetch('/static/jsonFilesGeneration/jsons_all/line1_all_exp.json')
        .then(function(res) {
            return res.json();
        })
])
    .then(function(dataArray) {
        var h = function(tag, attrs, children){
            var el = document.createElement(tag);

            Object.keys(attrs).forEach(function(key){
                var val = attrs[key];

                el.setAttribute(key, val);
            });

            children.forEach(function(child){
                el.appendChild(child);
            });

            return el;
        };

        var t = function(text){
            var el = document.createTextNode(text);

            return el;
        };

        var $ = document.querySelector.bind(document);

        var cy = window.cy = cytoscape({
            container: document.getElementById('cy'),
            style: dataArray[0],
            elements: dataArray[1],
            layout: { name: 'random' }
        });

        var params = {
            name: 'cola',
            nodeSpacing: 5,
            edgeLengthVal: 45,
            animate: true,
            randomize: false,
            maxSimulationTime: 1500
        };
        var layout = makeLayout();

        layout.run();

        function makeLayout( opts ){
            params.randomize = false;
            params.edgeLength = function(e){ return params.edgeLengthVal / e.data('weight'); };

            for( var i in opts ){
                params[i] = opts[i];
            }

            return cy.layout( params );
        }

        var makeTippy = function(node, html){
            return tippy( node.popperRef(), {
                html: html,
                trigger: 'manual',
                arrow: true,
                positionFixed: true,
                //placement: 'bottom',
                hideOnClick: false,
                interactive: true
            } ).tooltips[0];
        };

        var hideTippy = function(node){
            var tippy = node.data('tippy');

            if(tippy != null){
                tippy.hide();
            }
        };

        var hideAllTippies = function(){
            cy.nodes().forEach(hideTippy);
            cy.edges().forEach(hideTippy);
        };

        cy.on('tap', function(e){
            if(e.target === cy){
                hideAllTippies();
            }
        });


        cy.on('zoom pan', function(e){
            hideAllTippies();
        });

        cy.edges().forEach(function(n){
            var p = n.data('patients');

            var $links = [
                {
                    name: 'Patients: ' + p.toString().replace(/,/g, ',\n'),
                    url: p
                }
            ].map(function( link ){
                return h('div', { 'class': '' }, [ t(link.name) ]);
            });

            var tippy = makeTippy(n, h('div', {}, $links));

            n.data('tippy', tippy);

            n.on('select', function(e){
                tippy.show();

                cy.edges().not(n).forEach(hideTippy);
                cy.nodes().forEach(hideTippy);
            });

            n.on('unselect', function(e) {
                hideTippy(n);
            });
        });

        cy.nodes().forEach(function(n){
            var g = n.data('name');

            var p = n.data('patients');

            var $links = [
                {
                    name: 'Patients: ' + p.toString(),
                    url: p
                }
            ].map(function( link ){
                return h('a', { target: '_blank', href: link.url, 'class': 'tip-link' }, [ t(link.name) ]);
            });

            var tippy = makeTippy(n, h('div', {}, $links));

            n.data('tippy', tippy);

            n.on('click', function(e){
                tippy.show();

                cy.nodes().not(n).forEach(hideTippy);
            });
        });

        $('body').classList.toggle('config-closed');

        cy.resize();

    });
