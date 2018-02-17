var setup_tags_input = function(input) {
    var items;

    function loadJSON(url, callback) {
        var xobj = new XMLHttpRequest();
        xobj.open('GET', url, true);
        xobj.onreadystatechange = function () {
            if (xobj.readyState == 4 && xobj.status == "200") {
                callback(JSON.parse(xobj.responseText));
            }
        };
        xobj.send(null);
    }

    loadJSON('/static/js/citynames.json', function (json) {

        transform = function (json) {
            return $.map(json.items, function (item) {
                return {
                    name: item.name,
                    value2: item.id
                };
            });
        };

        data = transform(json)


        var countries = new Bloodhound({

            datumTokenizer: function (datum) {
                // console.log(datum)
                return Bloodhound.tokenizers.whitespace(datum.name)
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            local: data,
            remote: null && {
                // url: '/static/js/citynames.json',
                // transform: function (datum) {
                //     // debugger
                //     return $.map(datum.items, function (item) {
                //         return { value: item.name }
                //     });
                // }
                url: '/static/js/citynames.json',
                transform: function (response) {
                    // debugger;
                    // Map the remote source JSON array to a JavaScript object array
                    return $.map(response.results, function (movie) {
                        return {
                            value: movie.original_title,
                            value2: movie.popularity
                        };
                    });
                }
            }
        });

        countries.initialize();

        0 && $(input).typeahead(null, {
            // items:4,
            limit: 2,
            // name: 'countries',
            // source: countries,
            // displayKey: 'name',
            // displayKey: function (item){
            //    return item
            // },
            display: "name",
            // valueKey: 'name',
            source: countries.ttAdapter()
        });

        $(input).tagsinput({
            typeaheadjs: {
                name: 'countries',
                displayKey: 'name',
                valueKey: 'name',
                source: countries.ttAdapter()
            }
        });


        // $(input).bind('typeahead:render', function (ev, sugg, flag, name) {
        //     console.log('render: ', sugg, flag);
        // });
    }); // load
};
