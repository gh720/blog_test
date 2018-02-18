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

var setup_tags_input = function(input, current_items, items) {
    var transform = function (items) {
        return $.map(items, function (item) {
            // return {
            //     name: item.name,
            //     id: item.id
            // };
            return item.name;
        });
    };

    data = transform(items);
    var item_trie = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum);
            // return Bloodhound.tokenizers.whitespace(datum.name)
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: data
    });
    item_trie.initialize();

    console.log('current items:', data);

    var elt = $(input);

    elt.tagsinput({
        // itemValue: 'id',
        // itemText: 'name',
        // confirmKeys: [13, 32, 39, 188],
        typeaheadjs: {
            name: 'item_trie',
            // displayKey: 'name',
            // valueKey: 'name',
            source: item_trie.ttAdapter()
        }
    });
    for (var item of  current_items) {
        // var _item = {"name": item.name, "id": item.id};
        // console.log('added :', item);
        elt.tagsinput('add', item.name);
    }
    // $('.bootstrap-tagsinput input').on('keyup keypress', function(e){
    //     console.log('prevented!');
    //     if ((e.keyCode || e.which) == 13){
    //         e.preventDefault();
    //         return false;
    //     };
    // });


    // $(".twitter-typeahead > input").focus(function(){
    //     //disable btn when focusing the input
    //     $("#my_submit_button").prop('disabled', true);
    // }).blur(function(){
    //     //enable btn when bluring the input
    //     $("#my_submit_button").prop('disabled', false);
    // });


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

    $(input).find('#yes').one('click', closed);
    $(input).find('#cancel').one('click', closed);
    $(input).modal('show');

};

let confirm_items = function (old_items, new_items, input, show_excess_cb, cb) {
    excess_items = [];
    onames=$.map(old_items, function(v,i,a) { return v.name});
    // onames=$.map(old_items, function(v,i,a) { return v});
    for (var item of new_items) {
        if (onames.indexOf(item)==-1) {
            excess_items.push(item)
        }
    }
    if (excess_items.length == 0) {
        cb();
        return;
    }
    if (show_excess_cb) {
        show_excess_cb($.map(excess_items, function(v) { return '"'+v+'"'}).join(","));
    }
    ask_confirmation(input, cb);
};
