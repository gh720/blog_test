    if (1) {
        var movies = new Bloodhound({
            limit:1,
            datumTokenizer: function (datum) {
                console.log(datum)
                return Bloodhound.tokenizers.whitespace(datum.value);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: {
                // wildcard: '%QUERY',
                url: 'http://api.themoviedb.org/3/search/movie?query=b&api_key=f22e6ce68f5e5002e71c20bcba477e7d',
                // url: 'http://127.0.0.1:8002/static/js/citynames.json',
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

// Instantiate the Typeahead UI
        $('#typeahead3').typeahead(null, {
            display: 'value',
            source: movies
        });
    }
    if (0) {
        // instantiate the bloodhound suggestion engine
        var bloodhound = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            local: ["(A)labama", "Alaska", "Arizona", "Arkansas", "Arkansas2", "Barkansas"]
        });
        // initialize the bloodhound suggestion engine
        bloodhound.initialize();
        $('#typeahead2').typeahead(null,
            {
                items: 4,
                // , source: bloodhound,
                displayKey: function (item) {
                    return item
                },

                source: bloodhound.ttAdapter()
            });
    }
    if (0) {
        var states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
            'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
            'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
            'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
            'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
            'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
            'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
            'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
            'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        ];
        var citynames = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            prefetch: {
                url: '/static/js/citynames.json',
                filter: function (list) {
                    debugger;
                    return $.map(list, function (cityname) {
                        return {name: cityname};
                    });
                }
            }
            // local:states
        });
        citynames.initialize();

        $('input#tags_input').tagsinput({
            typeaheadjs: {
                name: 'citynames',
                displayKey: 'name',
                valueKey: 'name',
                source: citynames.ttAdapter()
            }
        });
    }

