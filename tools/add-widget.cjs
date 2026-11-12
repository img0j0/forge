// Adds the ForgelingsWidget extension (home-screen widget + wandering Live Activity) and the app's widget bridge to
// the Xcode project. Safe to run more than once. Needs the npm package "xcode" (npm i --no-save xcode@3.0.1).
const xcode=require('xcode'),fs=require('fs'),path=require('path');
const P=path.join(__dirname,'..','ios','App','App.xcodeproj','project.pbxproj');
const p=xcode.project(P);p.parseSync();
const targets=p.pbxNativeTargetSection();
const has=n=>Object.keys(targets).some(k=>!k.endsWith('_comment')&&targets[k].name&&targets[k].name.replace(/"/g,'')===n);
const appT=p.getFirstTarget().uuid,mainGroup=p.getFirstProject().firstProject.mainGroup;
const appGroupKey=Object.keys(p.hash.project.objects.PBXGroup).find(k=>{const g=p.hash.project.objects.PBXGroup[k];return g&&g.path==='App';});
function addSource(name,targetUuid,groupKey){ // a file in the App folder, compiled into a target
  const ref=p.generateUuid(),bld=p.generateUuid(),o=p.hash.project.objects;
  let fileRef=Object.keys(o.PBXFileReference).find(k=>!k.endsWith('_comment')&&o.PBXFileReference[k].path===name);
  if(!fileRef){fileRef=ref;o.PBXFileReference[ref]={isa:'PBXFileReference',lastKnownFileType:'sourcecode.swift',path:name,sourceTree:'"<group>"'};o.PBXFileReference[ref+'_comment']=name;
    o.PBXGroup[groupKey].children.push({value:ref,comment:name});}
  o.PBXBuildFile[bld]={isa:'PBXBuildFile',fileRef:fileRef,fileRef_comment:name};o.PBXBuildFile[bld+'_comment']=name+' in Sources';
  const t=o.PBXNativeTarget[targetUuid];const sp=t.buildPhases.find(b=>o.PBXSourcesBuildPhase[b.value]);
  o.PBXSourcesBuildPhase[sp.value].files.push({value:bld,comment:name+' in Sources'});}
if(!has('ForgelingsWidget')){
  const o=p.hash.project.objects;
  // the app: the bridge plugin and the shared Live Activity type; weak-link ActivityKit (the app still runs on iOS 15)
  addSource('WidgetBridgePlugin.swift',appT,appGroupKey);addSource('WanderAttributes.swift',appT,appGroupKey);
  for(const k in o.XCBuildConfiguration){const c=o.XCBuildConfiguration[k];if(k.endsWith('_comment')||!c.buildSettings||c.buildSettings.PRODUCT_BUNDLE_IDENTIFIER!=='com.forgelings.app')continue;
    c.buildSettings.OTHER_LDFLAGS=['"$(inherited)"','"-weak_framework"','ActivityKit'];}
  // the extension
  const t=p.addTarget('ForgelingsWidget','app_extension','ForgelingsWidget','com.forgelings.app.ForgelingsWidget');
  const grp=p.addPbxGroup(['ForgelingsWidget.swift','ForgelingsWidget-Info.plist','ForgelingsWidget.entitlements'],'ForgelingsWidget','ForgelingsWidget');
  o.PBXGroup[mainGroup].children.push({value:grp.uuid,comment:'ForgelingsWidget'});
  p.addBuildPhase(['ForgelingsWidget.swift'],'PBXSourcesBuildPhase','Sources',t.uuid);
  p.addBuildPhase([],'PBXFrameworksBuildPhase','Frameworks',t.uuid);
  p.addBuildPhase([],'PBXResourcesBuildPhase','Resources',t.uuid);
  // the shared type, compiled into the extension too
  const wa=Object.keys(o.PBXFileReference).find(k=>!k.endsWith('_comment')&&o.PBXFileReference[k].path==='WanderAttributes.swift');
  const bld=p.generateUuid();o.PBXBuildFile[bld]={isa:'PBXBuildFile',fileRef:wa,fileRef_comment:'WanderAttributes.swift'};o.PBXBuildFile[bld+'_comment']='WanderAttributes.swift in Sources';
  const sp=o.PBXNativeTarget[t.uuid].buildPhases.find(b=>o.PBXSourcesBuildPhase[b.value]);o.PBXSourcesBuildPhase[sp.value].files.push({value:bld,comment:'WanderAttributes.swift in Sources'});
  // build settings
  const cl=o.XCConfigurationList[o.PBXNativeTarget[t.uuid].buildConfigurationList].buildConfigurations.map(b=>b.value);
  for(const k of cl){Object.assign(o.XCBuildConfiguration[k].buildSettings,{
    CODE_SIGN_ENTITLEMENTS:'ForgelingsWidget/ForgelingsWidget.entitlements',CODE_SIGN_STYLE:'Automatic',CURRENT_PROJECT_VERSION:'1',MARKETING_VERSION:'1.0.0',
    IPHONEOS_DEPLOYMENT_TARGET:'16.2',SDKROOT:'iphoneos',SWIFT_VERSION:'5.0',TARGETED_DEVICE_FAMILY:'1',GENERATE_INFOPLIST_FILE:'NO',
    INFOPLIST_FILE:'ForgelingsWidget/ForgelingsWidget-Info.plist',ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME:'AccentColor',
    LD_RUNPATH_SEARCH_PATHS:'"$(inherited) @executable_path/Frameworks @executable_path/../../Frameworks"',SKIP_INSTALL:'YES',
    SWIFT_EMIT_LOC_STRINGS:'YES',DEVELOPMENT_LANGUAGE:'en'});
    delete o.XCBuildConfiguration[k].buildSettings.ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME;}
  // the app depends on and embeds the extension
  o.PBXContainerItemProxy=o.PBXContainerItemProxy||{};o.PBXTargetDependency=o.PBXTargetDependency||{};
  const proxy=p.generateUuid(),dep=p.generateUuid(),root=p.hash.project.rootObject;
  o.PBXContainerItemProxy[proxy]={isa:'PBXContainerItemProxy',containerPortal:root,containerPortal_comment:'Project object',proxyType:1,remoteGlobalIDString:t.uuid,remoteInfo:'ForgelingsWidget'};o.PBXContainerItemProxy[proxy+'_comment']='PBXContainerItemProxy';
  o.PBXTargetDependency[dep]={isa:'PBXTargetDependency',target:t.uuid,target_comment:'ForgelingsWidget',targetProxy:proxy,targetProxy_comment:'PBXContainerItemProxy'};o.PBXTargetDependency[dep+'_comment']='PBXTargetDependency';
  o.PBXNativeTarget[appT].dependencies.push({value:dep,comment:'PBXTargetDependency'});
  // tidy what the library writes: no "undefined" values, no stray build files for the plist and entitlements
  for(const k in o.PBXFileReference){const f=o.PBXFileReference[k];if(k.endsWith('_comment'))continue;for(const a in f)if(f[a]===undefined||f[a]==='undefined')delete f[a];}
  for(const k of Object.keys(o.PBXBuildFile)){if(k.endsWith('_comment'))continue;const c=o.PBXBuildFile[k+'_comment']||'';if(/ForgelingsWidget-Info\.plist|ForgelingsWidget\.entitlements/.test(c)){delete o.PBXBuildFile[k];delete o.PBXBuildFile[k+'_comment'];}}
  o.PBXNativeTarget[t.uuid].name='ForgelingsWidget';o.PBXNativeTarget[t.uuid].productName='ForgelingsWidget';o.PBXNativeTarget[t.uuid+'_comment']='ForgelingsWidget';
  for(const k in o.PBXCopyFilesBuildPhase){const ph=o.PBXCopyFilesBuildPhase[k];if(k.endsWith('_comment'))continue;if(ph.dstSubfolderSpec==13){ph.name='"Embed Foundation Extensions"';o.PBXCopyFilesBuildPhase[k+'_comment']='Embed Foundation Extensions';}}
  fs.writeFileSync(P,p.writeSync());console.log('ForgelingsWidget added');
}else console.log('ForgelingsWidget already in the project');
