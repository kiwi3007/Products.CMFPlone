from plone.protect import protect, CheckAuthenticator


def patch(callable):
    """ apply csrf-protection decorator to the given callable """
    return protect(callable, CheckAuthenticator)


def applyPatches():
    """ apply csrf-protection decorator to all relevant methods """

    from Products.CMFPlone.PloneTool import PloneTool as PT
    PT.setMemberProperties = patch(PT.setMemberProperties)
    PT.changeOwnershipOf = patch(PT.changeOwnershipOf)
    PT.acquireLocalRoles = patch(PT.acquireLocalRoles)
    PT.deleteObjectsByPaths = patch(PT.deleteObjectsByPaths)
    PT.transitionObjectsByPaths = patch(PT.transitionObjectsByPaths)
    PT.renameObjectsByPaths = patch(PT.renameObjectsByPaths)

    from plone.session.plugins.session import SessionPlugin as SP
    SP.manage_clearSecrets = patch(SP.manage_clearSecrets)
    SP.manage_createNewSecret = patch(SP.manage_createNewSecret)

    from Products.CMFCore.RegistrationTool import RegistrationTool
    RegistrationTool.addMember = patch(RegistrationTool.addMember)

    from Products.CMFCore.MembershipTool import MembershipTool as MT
    from Products.CMFPlone.MembershipTool import MembershipTool as PMT
    MT.setPassword = patch(MT.setPassword)
    PMT.setPassword = patch(PMT.setPassword)
    MT.setRoleMapping = patch(MT.setRoleMapping)
    MT.deleteMemberArea = patch(MT.deleteMemberArea)
    MT.setLocalRoles = patch(MT.setLocalRoles)
    MT.deleteLocalRoles = patch(MT.deleteLocalRoles)
    MT.deleteMembers = patch(MT.deleteMembers)

    from Products.CMFCore.MemberDataTool import MemberData as MD
    original_setProperties = MD.setProperties
    def setProperties(self, properties=None, REQUEST=None, **kw):
        return original_setProperties(self, properties, **kw)
    setProperties.__doc__ = original_setProperties.__doc__
    MD.setProperties = patch(setProperties)

    from Products.CMFDefault.RegistrationTool import RegistrationTool
    RegistrationTool.editMember = patch(RegistrationTool.editMember)

    from Products.PlonePAS.tools.groupdata import GroupData
    GroupData.addMember = patch(GroupData.addMember)
    GroupData.removeMember = patch(GroupData.removeMember)

    from Products.PluggableAuthService.PluggableAuthService import \
         PluggableAuthService as PAS
    PAS.userFolderAddUser = patch(PAS.userFolderAddUser)
    PAS.userFolderEditUser = patch(PAS.userFolderEditUser)
    PAS.userFolderDelUsers = patch(PAS.userFolderDelUsers)

