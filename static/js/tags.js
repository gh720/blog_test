var loadJSON = function (url, callback) {
    var xobj = new XMLHttpRequest();
    xobj.open('GET', url, true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(JSON.parse(xobj.responseText));
        }
    };
    xobj.send(null);
};

var setup_tags_input = function(input,items) {
    var transform = function (items) {
        return $.map(items, function (item) {
            return {
                name: item.name,
                id: item.id
            };
        });
    };

    data = transform(items);
    var item_trie = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum.name)
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: data
    });
    item_trie.initialize();

    console.log('current items:', data);

    $(input).tagsinput({
        typeaheadjs: {
            name: 'item_trie',
            displayKey: 'name',
            valueKey: 'name',
            source: item_trie.ttAdapter()
        }
    });


    // $(input).bind('typeahead:render', function (ev, sugg, flag, name) {
    //     console.log('render: ', sugg, flag);
    // });
; // load
};

var ask_confirmation=function (input, callback) {
    var closed=function(e) {
        var id = e.target && e.target.id;
        $(this).closest('.modal').one('hidden.bs.modal', callback(id))
    };

    $(input).children('#yes').one('click', closed);
    $(input).children('#cancel').one('click', closed);

};

let confirm_items = function (old_items, new_items, input, show_excess_cb, cb) {
    excess_items = [];
    for (var item of new_items) {
        if (!(item in old_items)) {
            excess_items.push(item)
        }
    }
    if (excess_items.length == 0) {
        cb();
        return;
    }
    if (show_excess_cb) {
        show_excess_cb(excess_items.join(","));
    }
    ask_confirmation(input, cb);
};
