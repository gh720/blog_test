var setup_tags_input_test = function(input) {
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

        var transform = function (json) {
            return $.map(json.items, function (item) {
                return {
                    name: item.name,
                    value2: item.id
                };
            });
        };

        data = transform(json);
        console.log('data', data)

        var citynames = new Bloodhound({

            datumTokenizer: function (datum) {
                console.log(datum)
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

        citynames.initialize();

        0 && $(input).typeahead(null, {
            // items:4,
            limit: 2,
            // name: 'citynames',
            // source: citynames,
            // displayKey: 'name',
            // displayKey: function (item){
            //    return item
            // },
            display: "name",
            // valueKey: 'name',
            source: citynames.ttAdapter()
        });

        console.log("instantiating tagsinput");
        1 && $(input).tagsinput({
            typeaheadjs: {
                name: 'citynames',
                displayKey: 'name',
                valueKey: 'name',
                source: citynames.ttAdapter()
            }
        });


        // $(input).bind('typeahead:render', function (ev, sugg, flag, name) {
        //     console.log('render: ', sugg, flag);
        // });
    }); // load
};
