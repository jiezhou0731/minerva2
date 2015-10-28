if(andrewThree === undefined) {
  var andrewThree = {};
}
/*
test= andrewThree.ObjectContainer();
test.addTo(scene);
test.render();
*/
andrewThree.ObjectContainer=function(){
    var objectContainer={};
    objectContainer.objectList=[];
    objectContainer.clickableList=[];

    objectContainer.push=function(object){
        objectContainer.objectList.push(object);
        if (object.getClickable()!=undefined) {
            for (var i=0; i<object.getClickable().length; i++) {
                objectContainer.clickableList.push(object.getClickable()[i]);
            }
        }
    }

    objectContainer.addTo = function(scene){
        for (var i=0; i<objectContainer.objectList.length; i++) {
            objectContainer.objectList[i].addTo(scene);
        }
    }

    objectContainer.removeAll = function(scene){
        while (scene.children.length!=0){
            for (var i=0; i<scene.children.length; i++){
                scene.remove(scene.children[i]);
            }
        }
        objectContainer.clickableList=[];
    }

    objectContainer.render = function(delta){
        for (var i=0; i<objectContainer.objectList.length; i++) {
            objectContainer.objectList[i].render(delta);
        }
    }

    objectContainer.searchByDataId = function(id){
        for (var i=0; i<objectContainer.objectList.length; i++) {
            if (objectContainer.objectList[i].data['id']==id) {
                return objectContainer.objectList[i];
            }
        } 
        return undefined;
    }

    objectContainer.openAll = function(){
        for (var i=0; i<objectContainer.objectList.length; i++) {
            if (objectContainer.objectList[i].isOpen==false) {
                objectContainer.objectList[i].open();
            }
        } 
    }

    objectContainer.closeAll = function(){
        for (var i=0; i<objectContainer.objectList.length; i++) {
            if (objectContainer.objectList[i].isOpen==true) {
                objectContainer.objectList[i].close();
            }
        } 
    }

    objectContainer.removeHighlight = function(){
        for (var i=0; i<objectContainer.objectList.length; i++) {
            if (objectContainer.objectList[i].removeHighlight!=undefined) {
                objectContainer.objectList[i].removeHighlight();
            }
        } 
    }

    return objectContainer;
}