// Old browsers, like IE 11, don't have this function I use
if (!document.getElementsByClassName) {
    document.getElementsByClassName = function(cl) {
      var retnode = [];
      var elem = this.getElementsByTagName('*');
      for (var i = 0; i < elem.length; i++) {
        if((' ' + elem[i].className + ' ').indexOf(' ' + cl + ' ') > -1) retnode.push(elem[i]);
      }
      return retnode;
    }
};
