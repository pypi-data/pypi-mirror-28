from .future import DSSFuture

class DSSConnection(object):
    """
    A connection on the DSS instance
    """
    def __init__(self, client, name):
        self.client = client
        self.name = name
    
    ########################################################
    # User deletion
    ########################################################
    
    def delete(self):
        """
        Delete the connection

        Note: this call requires an API key with admin rights
        """
        return self.client._perform_empty(
            "DELETE", "/admin/connections/%s" % self.name)
    
        
    ########################################################
    # User description
    ########################################################
    
    def get_definition(self):
        """
        Get the connection's definition (type, name, params, usage restrictions)

        Note: this call requires an API key with admin rights
        
        Returns:
            the connection definition, as a JSON object
        """
        return self.client._perform_json(
            "GET", "/admin/connections/%s" % self.name)
    
    def set_definition(self, description):
        """
        Set the connection's definition.
        
        Note: this call requires an API key with admin rights
        
        Args:
            definition: the definition for the connection, as a JSON object.            
        """
        return self.client._perform_json(
            "PUT", "/admin/connections/%s" % self.name,
            body = description)
    
    ########################################################
    # Security
    ########################################################
    
    def sync_root_acls(self):
        """
        Resync root permissions on this connection path
        
        Returns:
            a DSSFuture handle to the task of resynchronizing the permissions
        
        Note: this call requires an API key with admin rights
        """
        future_response = self.client._perform_json(
            "POST", "/admin/connections/%s/sync" % self.name,
            body = {'root':True})
        return DSSFuture(self.client, future_response.get('jobId', None), future_response)
    
    def sync_datasets_acls(self):
        """
        Resync permissions on datasets in this connection path
        
        Returns:
            a DSSFuture handle to the task of resynchronizing the permissions
        
        Note: this call requires an API key with admin rights
        """
        future_response = self.client._perform_json(
            "POST", "/admin/connections/%s/sync" % self.name,
            body = {'root':True})
        return DSSFuture(self.client, future_response.get('jobId', None), future_response)
    
        
class DSSUser(object):
    """
    A handle for a user on the DSS instance
    """
    def __init__(self, client, login):
        self.client = client
        self.login = login

    ########################################################
    # User deletion
    ########################################################

    def delete(self):
        """
        Deletes the user

        Note: this call requires an API key with admin rights
        """
        return self.client._perform_empty(
            "DELETE", "/admin/users/%s" % self.login)

    ########################################################
    # User description
    ########################################################

    def get_definition(self):
        """
        Get the user's definition (login, type, display name, permissions, ...)

        Note: this call requires an API key with admin rights

        :return: the user's definition, as a dict
        """
        return self.client._perform_json(
            "GET", "/admin/users/%s" % self.login)

    def set_definition(self, definition):
        """
        Set the user's definition.

        Note: this call requires an API key with admin rights

        :param dict definition: the definition for the user, as a dict. You should
            obtain the definition using get_definition, not create one.
            The fields that can be changed are:
                
                * email
                
                * displayName
                
                * groups
                
                * userProfile
                
                * password

        """
        return self.client._perform_json(
            "PUT", "/admin/users/%s" % self.login,
            body = definition)
            
class DSSGroup(object):
    """
    A group on the DSS instance
    """
    def __init__(self, client, name):
        self.client = client
        self.name = name
    
    ########################################################
    # Group deletion
    ########################################################
    
    def delete(self):
        """
        Delete the group

        Note: this call requires an API key with admin rights
        """
        return self.client._perform_empty(
            "DELETE", "/admin/groups/%s" % self.name)
    
        
    ########################################################
    # User description
    ########################################################
    
    def get_definition(self):
        """
        Get the group's definition (name, description, admin abilities, type, ldap name mapping)

        Note: this call requires an API key with admin rights
        
        Returns:
            the group definition, as a JSON object
        """
        return self.client._perform_json(
            "GET", "/admin/groups/%s" % self.name)
    
    def set_definition(self, definition):
        """
        Set the group's definition.
        
        Note: this call requires an API key with admin rights
        
        Args:
            definition: the definition for the group, as a JSON object.                        
        """
        return self.client._perform_json(
            "PUT", "/admin/groups/%s" % self.name,
            body = definition)
    
        
class DSSGeneralSettings(object):
    """
    The general settings of the DSS instance
    """
    def __init__(self, client):
        self.client = client
        self.settings = self.client._perform_json("GET", "/admin/general-settings")
    
    ########################################################
    # Update settings on instance
    ########################################################
    
    def save(self):
        """
        Save the changes that were made to the settings on the DSS instance

        Note: this call requires an API key with admin rights
        """
        return self.client._perform_empty("PUT", "/admin/general-settings", body = self.settings)
    
    
    ########################################################
    # Value accessors
    ########################################################
    
    def get_raw(self):
        """
        Get the settings as a dictionary
        """
        return self.settings

    def add_impersonation_rule(self, rule, is_user_rule=True):
        """
        Add a rule to the impersonation settings

        :param rule: an impersonation rule, either a :class:`dataikuapi.dss.admin.DSSUserImpersonationRule`
            or a :class:`dataikuapi.dss.admin.DSSGroupImpersonationRule`, or a plain dict
        :param is_user_rule: when the rule parameter is a dict, whether the rule is for users or groups
        """
        rule_raw = rule
        if isinstance(rule, DSSUserImpersonationRule):
            rule_raw = rule.raw
            is_user_rule = True
        elif isinstance(rule, DSSGroupImpersonationRule):
            rule_raw = rule.raw
            is_user_rule = False
        impersonation = self.settings['impersonation']
        if is_user_rule:
            impersonation['userRules'].append(rule_raw)
        else:
            impersonation['groupRules'].append(rule_raw)

    def get_impersonation_rules(self, dss_user=None, dss_group=None, unix_user=None, hadoop_user=None, project_key=None, scope=None, rule_type=None, is_user=None):
        """
        Retrieve the user or group impersonation rules that matches the parameters

        :param dss_user: a DSS user or regular expression to match DSS user names
        :param dss_group: a DSS group or regular expression to match DSS groups
        :param unix_user: a name to match the target UNIX user
        :param hadoop_user: a name to match the target Hadoop user
        :param project_key: a project_key
        :param scope: project-scoped ('PROJECT') or global ('GLOBAL')
        :param type: the rule user or group matching method ('IDENTITY', 'SINGLE_MAPPING', 'REGEXP_RULE')
        :param is_user: True if only user-level rules should be considered, False for only group-level rules, None to consider both
        """
        user_matches = self.settings['impersonation']['userRules'] if is_user == None or is_user == True else []
        if dss_user is not None:
            user_matches = [m for m in user_matches if dss_user == m.get('dssUser', None)]
        if unix_user is not None:
            user_matches = [m for m in user_matches if unix_user == m.get('targetUnix', None)]
        if hadoop_user is not None:
            user_matches = [m for m in user_matches if hadoop_user == m.get('targetHadoop', None)]
        if project_key is not None:
            user_matches = [m for m in user_matches if project_key == m.get('projectKey', None)]
        if rule_type is not None:
            user_matches = [m for m in user_matches if rule_type == m.get('type', None)]
        if scope is not None:
            user_matches = [m for m in user_matches if scope == m.get('scope', None)]
        group_matches = self.settings['impersonation']['groupRules'] if is_user == None or is_user == False else []
        if dss_group is not None:
            group_matches = [m for m in group_matches if dss_group == m.get('dssGroup', None)]
        if unix_user is not None:
            group_matches = [m for m in group_matches if unix_user == m.get('targetUnix', None)]
        if hadoop_user is not None:
            group_matches = [m for m in group_matches if hadoop_user == m.get('targetHadoop', None)]
        if rule_type is not None:
            group_matches = [m for m in group_matches if rule_type == m.get('type', None)]

        all_matches = []
        for m in user_matches:
            all_matches.append(DSSUserImpersonationRule(m))
        for m in group_matches:
            all_matches.append(DSSGroupImpersonationRule(m))
        return all_matches

    def remove_impersonation_rules(self, dss_user=None, dss_group=None, unix_user=None, hadoop_user=None, project_key=None, scope=None, rule_type=None, is_user=None):
        """
        Remove the user or group impersonation rules that matches the parameters from the settings

        :param dss_user: a DSS user or regular expression to match DSS user names
        :param dss_group: a DSS group or regular expression to match DSS groups
        :param unix_user: a name to match the target UNIX user
        :param hadoop_user: a name to match the target Hadoop user
        :param project_key: a project_key
        :param scope: project-scoped ('PROJECT') or global ('GLOBAL')
        :param type: the rule user or group matching method ('IDENTITY', 'SINGLE_MAPPING', 'REGEXP_RULE')
        :param is_user: True if only user-level rules should be considered, False for only group-level rules, None to consider both
        """
        for m in self.get_impersonation_rules(dss_user, dss_group, unix_user, hadoop_user, project_key, scope, rule_type, is_user):
            if isinstance(m, DSSUserImpersonationRule):
                self.settings['impersonation']['userRules'].remove(m.raw)
            elif isinstance(m, DSSGroupImpersonationRule):
                self.settings['impersonation']['groupRules'].remove(m.raw)


class DSSUserImpersonationRule(object):
    """
    Helper to build user-level rule items for the impersonation settings
    """
    def __init__(self, raw=None):
        self.raw = raw if raw is not None else {'scope':'GLOBAL','type':'IDENTITY'}

    def scope_global(self):
        """
        Make the rule apply to all projects
        """
        self.raw['scope'] = 'GLOBAL'
        return self

    def scope_project(self, project_key):
        """
        Make the rule apply to a given project

        Args:
            project_key : the project this rule applies to
        """
        self.raw['scope'] = 'PROJECT'
        self.raw['projectKey'] = project_key
        return self

    def user_identity(self):
        """
        Make the rule map each DSS user to a UNIX user of the same name
        """
        self.raw['type'] = 'IDENTITY'
        return self

    def user_single(self, dss_user, unix_user, hadoop_user=None):
        """
        Make the rule map a given DSS user to a given UNIX user

        Args:
            dss_user : a DSS user
            unix_user : a UNIX user
            hadoop_user : a Hadoop user (optional, defaults to unix_user)
        """
        self.raw['type'] = 'SINGLE_MAPPING'
        self.raw['dssUser'] = dss_user
        self.raw['targetUnix'] = unix_user
        self.raw['targetHadoop'] = hadoop_user
        return self

    def user_regexp(self, regexp, unix_user, hadoop_user=None):
        """
        Make the rule map a DSS users matching a given regular expression to a given UNIX user

        Args:
            regexp : a regular expression to match DSS user names
            unix_user : a UNIX user
            hadoop_user : a Hadoop user (optional, defaults to unix_user)
        """
        self.raw['type'] = 'REGEXP_RULE'
        self.raw['ruleFrom'] = regexp
        self.raw['targetUnix'] = unix_user
        self.raw['targetHadoop'] = hadoop_user
        return self

class DSSGroupImpersonationRule(object):
    """
    Helper to build group-level rule items for the impersonation settings
    """
    def __init__(self, raw=None):
        self.raw = raw if raw is not None else {'type':'IDENTITY'}

    def group_identity(self):
        """
        Make the rule map each DSS user to a UNIX user of the same name
        """
        self.raw['type'] = 'IDENTITY'
        return self

    def group_single(self, dss_group, unix_user, hadoop_user=None):
        """
        Make the rule map a given DSS user to a given UNIX user

        Args:
            dss_group : a DSS group
            unix_user : a UNIX user
            hadoop_user : a Hadoop user (optional, defaults to unix_user)
        """
        self.raw['type'] = 'SINGLE_MAPPING'
        self.raw['dssGroup'] = dss_group
        self.raw['targetUnix'] = unix_user
        self.raw['targetHadoop'] = hadoop_user
        return self

    def group_regexp(self, regexp, unix_user, hadoop_user=None):
        """
        Make the rule map a DSS users matching a given regular expression to a given UNIX user

        Args:
            regexp : a regular expression to match DSS groups
            unix_user : a UNIX user
            hadoop_user : a Hadoop user (optional, defaults to unix_user)
        """
        self.raw['type'] = 'REGEXP_RULE'
        self.raw['ruleFrom'] = regexp
        self.raw['targetUnix'] = unix_user
        self.raw['targetHadoop'] = hadoop_user
        return self
