# -*- coding: utf-8 -*-
from comport.database import (Column, db, Model, SurrogatePK)
from .cleaners import Cleaners
from comport.utils import parse_date, parse_int

#
# DENOMINATOR VALUES
#

class DenominatorValue(SurrogatePK, Model):
    __tablename__ = "denominator_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    month = Column(db.Integer, unique=False, nullable=False)
    year = Column(db.Integer, unique=False, nullable=False)
    officers_out_on_service = Column(db.Integer, unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

#
# DEMOGRAPHIC VALUES
#

class DemographicValue(SurrogatePK, Model):
    __tablename__ = "demographic_values"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    race = Column(db.String(255), unique=False, nullable=True)
    count = Column(db.Integer, unique=False, nullable=True)
    department_value = Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

#
# INCIDENTS UPDATED
#

class IncidentsUpdated(SurrogatePK, Model):
    __tablename__ = "incidents_updated"
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False, index=True)
    incident_type = Column(db.String(32), unique=False, nullable=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def delete_records(cls, department_id=None, incident_type=None):
        ''' Delete IncidentsUpdated records matching the passed parameters
        '''
        if not department_id:
            return 0

        kwargs = dict(department_id=department_id)
        if incident_type:
            kwargs['incident_type'] = incident_type

        deleted_count = cls.query.filter_by(**kwargs).delete()
        db.session.commit()

        return deleted_count

#
# INDIANAPOLIS METRO POLICE DEPARTMENT
#

class UseOfForceIncidentIMPD(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    resident_resist_type = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("division", "division", "division"),
            ("district", "precinct", "precinct"),
            ("shift", "shift", "shift"),
            ("beat", "beat", "beat"),
            ("useOfForceReason", "use_of_force_reason", "useOfForceReason"),
            ("officerForceType", "officer_force_type", "officerForceType"),
            ("disposition", "disposition", "disposition"),
            ("serviceType", "service_type", "serviceType"),
            ("arrestMade", "arrest_made", "arrestMade"),
            ("arrestCharges", "arrest_charges", "arrestCharges"),
            ("residentInjured", "resident_injured", "residentInjured"),
            ("residentHospitalized", "resident_hospitalized", "residentHospitalized"),
            ("residentCondition", "resident_condition", "residentCondition"),
            ("officerInjured", "officer_injured", "officerInjured"),
            ("officerHospitalized", "officer_hospitalized", "officerHospitalized"),
            ("officerCondition", "officer_condition", "officerCondition"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new UOF incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["precinct"] = cleaner.capitalize(incident["precinct"])
        incident["shift"] = cleaner.capitalize(incident["shift"])
        incident["beat"] = cleaner.capitalize(incident["beat"])
        # clean force type, race, gender
        incident["officerForceType"] = cleaner.officer_force_type(incident["officerForceType"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])

        found_incident = cls.query.filter_by(
            opaque_id=incident["opaqueId"],
            department_id=department.id,
            officer_identifier=incident["officerIdentifier"],
            officer_force_type=incident["officerForceType"]
        ).first()

        if not found_incident:
            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"])
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.division = incident["division"]
        found_incident.precinct = incident["precinct"]
        found_incident.shift = incident["shift"]
        found_incident.beat = incident["beat"]
        found_incident.disposition = incident["disposition"]
        found_incident.census_tract = None
        found_incident.officer_force_type = incident["officerForceType"]
        found_incident.use_of_force_reason = incident["useOfForceReason"]
        found_incident.service_type = incident["serviceType"]
        found_incident.arrest_made = incident["arrestMade"]
        found_incident.arrest_charges = incident["arrestCharges"]
        found_incident.resident_weapon_used = incident["residentWeaponUsed"]
        found_incident.resident_injured = incident["residentInjured"]
        found_incident.resident_hospitalized = incident["residentHospitalized"]
        found_incident.officer_injured = incident["officerInjured"]
        found_incident.officer_hospitalized = incident["officerHospitalized"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.resident_condition = incident["residentCondition"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = incident["officerYearsOfService"]
        found_incident.officer_condition = incident["officerCondition"]
        found_incident.save()

        return row_added

class AssaultOnOfficerIMPD(SurrogatePK, Model):
    __tablename__ = 'assaults_on_officers_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    force_type = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_killed = Column(db.Boolean, nullable=True)
    report_filed = Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier"),
            ("serviceType", "service_type", "serviceType"),
            ("forceType", "force_type", "forceType"),
            ("assignment", "assignment", "assignment"),
            ("arrestMade", "arrest_made", "arrestMade"),
            ("officerInjured", "officer_injured", "officerInjured"),
            ("officerKilled", "officer_killed", "officerKilled"),
            ("reportFiled", "report_filed", "reportFiled")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Assaults on Officers incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)

        found_incident = cls.query.filter_by(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            officer_identifier=incident["officerIdentifier"]
        ).first()

        if not found_incident:

            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )

            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.service_type = incident["serviceType"]
        found_incident.force_type = incident["forceType"]
        found_incident.force_type = incident["forceType"]
        found_incident.assignment = incident["assignment"]
        found_incident.arrest_made = incident["arrestMade"]
        found_incident.officer_injured = incident["officerInjured"]
        found_incident.officer_killed = incident["officerKilled"]
        found_incident.report_filed = incident["reportFiled"]
        found_incident.save()

        return row_added

class CitizenComplaintIMPD(SurrogatePK, Model):
    __tablename__ = 'citizen_complaints_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    source = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    allegation_type = Column(db.String(255), unique=False, nullable=True)
    allegation = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("division", "division", "division"),
            ("district", "precinct", "precinct"),
            ("shift", "shift", "shift"),
            ("beat", "beat", "beat"),
            ("serviceType", "service_type", "serviceType"),
            ("source", "source", "source"),
            ("allegationType", "allegation_type", "allegationType"),
            ("allegation", "allegation", "allegation"),
            ("finding", "disposition", "disposition"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Citizen Complaints incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)
        # clean sex & race
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])

        found_incident = cls.query.filter_by(
            opaque_id=incident["opaqueId"],
            allegation_type=incident["allegationType"],
            allegation=incident["allegation"],
            officer_identifier=incident["officerIdentifier"],
            department_id=department.id,
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"]
        ).first()

        if not found_incident:

            # check for multiple complainants
            # :TODO: validate this practice!
            multiple_complaintant_check = cls.query.filter_by(
                opaque_id=incident["opaqueId"],
                allegation_type=incident["allegationType"],
                allegation=incident["allegation"],
                officer_identifier=incident["officerIdentifier"],
                department_id=department.id
            ).first()

            if multiple_complaintant_check:
                return None

            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.service_type = incident["serviceType"]
        found_incident.source = incident["source"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.division = incident["division"]
        found_incident.precinct = incident["precinct"]
        found_incident.shift = incident["shift"]
        found_incident.beat = incident["beat"]
        found_incident.allegation_type = incident["allegationType"]
        found_incident.allegation = incident["allegation"]
        found_incident.disposition = incident["disposition"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = incident["officerYearsOfService"]
        found_incident.census_tract = None
        found_incident.save()

        return row_added

class OfficerInvolvedShootingIMPD(SurrogatePK, Model):
    __tablename__ = 'officer_involved_shootings_impd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    precinct = Column(db.String(255), unique=False, nullable=True)
    shift = Column(db.String(255), unique=False, nullable=True)
    beat = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    census_tract = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("division", "division", "division"),
            ("district", "precinct", "precinct"),
            ("shift", "shift", "shift"),
            ("beat", "beat", "beat"),
            ("disposition", "disposition", "disposition"),
            ("residentWeaponUsed", "resident_weapon_used", "residentWeaponUsed"),
            ("officerWeaponUsed", "officer_weapon_used", "officerWeaponUsed"),
            ("serviceType", "service_type", "serviceType"),
            ("residentCondition", "resident_condition", "residentCondition"),
            ("officerCondition", "officer_condition", "officerCondition"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new OIS incident or update an existing one
        '''
        row_added = False
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["precinct"] = cleaner.capitalize(incident["precinct"])
        incident["shift"] = cleaner.capitalize(incident["shift"])
        incident["beat"] = cleaner.capitalize(incident["beat"])
        # clean weapon, race, gender
        incident["residentWeaponUsed"] = cleaner.resident_weapon_used(incident["residentWeaponUsed"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        # and values that might've been sent as strings are integers
        incident["officerYearsOfService"] = cleaner.string_to_integer(incident["officerYearsOfService"])

        found_incident = cls.query.filter_by(
            opaque_id=incident["opaqueId"],
            department_id=department.id,
            officer_identifier=incident["officerIdentifier"]
        ).first()

        if not found_incident:
            found_incident = cls.create(
                department_id=department.id,
                opaque_id=incident["opaqueId"]
            )
            row_added = True

        found_incident.department_id = department.id
        found_incident.opaque_id = incident["opaqueId"]
        found_incident.service_type = incident["serviceType"]
        found_incident.occured_date = parse_date(incident["occuredDate"])
        found_incident.division = incident["division"]
        found_incident.precinct = incident["precinct"]
        found_incident.shift = incident["shift"]
        found_incident.beat = incident["beat"]
        found_incident.disposition = incident["disposition"]
        found_incident.resident_race = incident["residentRace"]
        found_incident.resident_sex = incident["residentSex"]
        found_incident.resident_age = incident["residentAge"]
        found_incident.resident_weapon_used = incident["residentWeaponUsed"]
        found_incident.resident_condition = incident["residentCondition"]
        found_incident.officer_identifier = incident["officerIdentifier"]
        found_incident.officer_weapon_used = incident["officerForceType"]
        found_incident.officer_race = incident["officerRace"]
        found_incident.officer_sex = incident["officerSex"]
        found_incident.officer_age = incident["officerAge"]
        found_incident.officer_years_of_service = parse_int(incident["officerYearsOfService"])
        found_incident.officer_condition = incident["officerCondition"]
        found_incident.census_tract = None
        found_incident.save()

        return row_added

#
# BALTIMORE POLICE DEPARTMENT
#

class UseOfForceIncidentBPD(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents_bpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(128), unique=False, nullable=True)
    occured_date = Column(db.DateTime, nullable=True)
    received_date = Column(db.DateTime, nullable=True)
    completed_date = Column(db.DateTime, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("receivedDate", "received_date", "receivedDate"),
            ("completedDate", "completed_date", "completedDate"),
            ("assignment", "assignment", "assignment"),
            ("useOfForceReason", "use_of_force_reason", "useOfForceReason"),
            ("officerForceType", "officer_force_type", "officerForceType"),
            ("serviceType", "service_type", "serviceType"),
            ("arrestMade", "arrest_made", "arrestMade"),
            ("arrestCharges", "arrest_charges", "arrestCharges"),
            ("residentInjured", "resident_injured", "residentInjured"),
            ("residentHospitalized", "resident_hospitalized", "residentHospitalized"),
            ("residentCondition", "resident_condition", "residentCondition"),
            ("officerInjured", "officer_injured", "officerInjured"),
            ("officerHospitalized", "officer_hospitalized", "officerHospitalized"),
            ("officerCondition", "officer_condition", "officerCondition"),
            ("residentIdentifier", "resident_identifier", "residentIdentifier"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new UOF incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the assignment
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean force type, race, gender
        incident["officerForceType"] = cleaner.officer_force_type(incident["officerForceType"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="uof")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        # create the new incident row
        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            case_number=incident["caseNumber"],
            occured_date=parse_date(incident["occuredDate"]),
            received_date=parse_date(incident["receivedDate"]),
            completed_date=parse_date(incident["completedDate"]),
            assignment=incident["assignment"],
            use_of_force_reason=incident["useOfForceReason"],
            officer_force_type=incident["officerForceType"],
            service_type=incident["serviceType"],
            arrest_made=incident["arrestMade"],
            arrest_charges=incident["arrestCharges"],
            resident_injured=incident["residentInjured"],
            resident_hospitalized=incident["residentHospitalized"],
            resident_condition=incident["residentCondition"],
            officer_injured=incident["officerInjured"],
            officer_hospitalized=incident["officerHospitalized"],
            officer_condition=incident["officerCondition"],
            resident_identifier=incident["residentIdentifier"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            officer_race=incident["officerRace"],
            officer_sex=incident["officerSex"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"],
            officer_identifier=incident["officerIdentifier"]
        )

        # TODO: re-evaluate what this return value means
        return True

class CitizenComplaintBPD(SurrogatePK, Model):
    __tablename__ = 'citizen_complaints_bpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(128), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    incident_type = Column(db.String(128), unique=False, nullable=True)
    source = Column(db.String(255), unique=False, nullable=True)
    occured_date = Column(db.DateTime, nullable=True)
    received_date = Column(db.DateTime, nullable=True)
    completed_date = Column(db.DateTime, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    allegation = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_role = Column(db.String(128), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("serviceType", "service_type", "serviceType"),
            ("incidentType", "incident_type", "incidentType"),
            ("source", "source", "source"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("receivedDate", "received_date", "receivedDate"),
            ("completedDate", "completed_date", "completedDate"),
            ("assignment", "assignment", "assignment"),
            ("allegation", "allegation", "allegation"),
            ("disposition", "disposition", "disposition"),
            ("residentIdentifier", "resident_identifier", "residentIdentifier"),
            ("residentRole", "resident_role", "residentRole"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Citizen Complaints incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)
        # clean sex & race
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="complaints")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        # create the new incident row
        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            case_number=incident["caseNumber"],
            service_type=incident["serviceType"],
            incident_type=incident["incidentType"],
            source=incident["source"],
            occured_date=parse_date(incident["occuredDate"]),
            received_date=parse_date(incident["receivedDate"]),
            completed_date=parse_date(incident["completedDate"]),
            assignment=incident["assignment"],
            allegation=incident["allegation"],
            disposition=incident["disposition"],
            resident_identifier=incident["residentIdentifier"],
            resident_role=incident["residentRole"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            officer_identifier=incident["officerIdentifier"],
            officer_race=incident["officerRace"],
            officer_sex=incident["officerSex"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"],
        )

        # TODO: re-evaluate what this return value means
        return True

class OfficerInvolvedShootingBPD(SurrogatePK, Model):
    __tablename__ = 'officer_involved_shootings_bpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    occured_date = Column(db.DateTime, nullable=True)
    received_date = Column(db.DateTime, nullable=True)
    completed_date = Column(db.DateTime, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    has_disposition = Column(db.Boolean, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    resident_weapon_used = Column(db.String(255), unique=False, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.Integer, unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("serviceType", "service_type", "serviceType"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("receivedDate", "received_date", "receivedDate"),
            ("completedDate", "completed_date", "completedDate"),
            ("assignment", "assignment", "assignment"),
            ("hasDisposition", "has_disposition", "hasDisposition"),
            ("residentIdentifier", "resident_identifier", "residentIdentifier"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("residentWeaponUsed", "resident_weapon_used", "residentWeaponUsed"),
            ("residentCondition", "resident_condition", "residentCondition"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("officerWeaponUsed", "officer_weapon_used", "officerWeaponUsed"),
            ("officerCondition", "officer_condition", "officerCondition")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new OIS incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the assignment
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean weapon, race, gender
        incident["residentWeaponUsed"] = cleaner.resident_weapon_used(incident["residentWeaponUsed"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        # and values that might've been sent as strings are integers
        incident["officerYearsOfService"] = cleaner.string_to_integer(incident["officerYearsOfService"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="ois")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            case_number=incident["caseNumber"],
            service_type=incident["serviceType"],
            occured_date=parse_date(incident["occuredDate"]),
            received_date=parse_date(incident["receivedDate"]),
            completed_date=parse_date(incident["completedDate"]),
            assignment=incident["assignment"],
            has_disposition=incident["hasDisposition"],
            resident_identifier=incident["residentIdentifier"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            resident_weapon_used=incident["residentWeaponUsed"],
            resident_condition=incident["residentCondition"],
            officer_identifier=incident["officerIdentifier"],
            officer_race=incident["officerRace"],
            officer_sex=incident["officerSex"],
            officer_age=incident["officerAge"],
            officer_years_of_service=parse_int(incident["officerYearsOfService"]),
            officer_weapon_used=incident["officerWeaponUsed"],
            officer_condition=incident["officerCondition"]
        )

        # TODO: re-evaluate what this return value means
        return True

#
# LOUISVILLE METRO POLICE DEPARTMENT
#

class UseOfForceIncidentLMPD(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents_lmpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    occured_date = Column(db.DateTime, nullable=True)
    bureau = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    unit = Column(db.String(255), unique=False, nullable=True)
    platoon = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    arrest_charges = Column(db.String(255), unique=False, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    resident_identifier = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_race = Column(db.String(255), unique=False, nullable=True)
    officer_sex = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    officer_identifier = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("occurredDate", "occured_date", "occuredDate"),
            ("bureau", "bureau", "bureau"),
            ("division", "division", "division"),
            ("unit", "unit", "unit"),
            ("platoon", "platoon", "platoon"),
            ("disposition", "disposition", "disposition"),
            ("useOfForceReason", "use_of_force_reason", "useOfForceReason"),
            ("officerForceType", "officer_force_type", "officerForceType"),
            ("serviceType", "service_type", "serviceType"),
            ("arrestMade", "arrest_made", "arrestMade"),
            ("arrestCharges", "arrest_charges", "arrestCharges"),
            ("residentInjured", "resident_injured", "residentInjured"),
            ("residentHospitalized", "resident_hospitalized", "residentHospitalized"),
            ("residentCondition", "resident_condition", "residentCondition"),
            ("officerInjured", "officer_injured", "officerInjured"),
            ("officerHospitalized", "officer_hospitalized", "officerHospitalized"),
            ("officerCondition", "officer_condition", "officerCondition"),
            ("residentIdentifier", "resident_identifier", "residentIdentifier"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerRace", "officer_race", "officerRace"),
            ("officerSex", "officer_sex", "officerSex"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("officerIdentifier", "officer_identifier", "officerIdentifier")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new UOF incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["bureau"] = cleaner.capitalize(incident["bureau"])
        incident["division"] = cleaner.capitalize(incident["division"])
        incident["unit"] = cleaner.capitalize(incident["unit"])
        incident["platoon"] = cleaner.capitalize(incident["platoon"])
        # clean force type, race, gender
        incident["officerForceType"] = cleaner.officer_force_type(incident["officerForceType"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["officerRace"] = cleaner.race(incident["officerRace"])
        incident["officerSex"] = cleaner.sex(incident["officerSex"])
        # make sure values that might've been sent as integers are strings
        incident["residentAge"] = cleaner.number_to_string(incident["residentAge"])
        incident["officerAge"] = cleaner.number_to_string(incident["officerAge"])
        incident["officerYearsOfService"] = cleaner.number_to_string(incident["officerYearsOfService"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="uof")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            occured_date=parse_date(incident["occuredDate"]),
            bureau=incident["bureau"],
            division=incident["division"],
            unit=incident["unit"],
            platoon=incident["platoon"],
            disposition=incident["disposition"],
            use_of_force_reason=incident["useOfForceReason"],
            officer_force_type=incident["officerForceType"],
            service_type=incident["serviceType"],
            arrest_made=incident["arrestMade"],
            arrest_charges=incident["arrestCharges"],
            resident_injured=incident["residentInjured"],
            resident_hospitalized=incident["residentHospitalized"],
            resident_condition=incident["residentCondition"],
            officer_injured=incident["officerInjured"],
            officer_hospitalized=incident["officerHospitalized"],
            officer_condition=incident["officerCondition"],
            resident_identifier=incident["residentIdentifier"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            officer_race=incident["officerRace"],
            officer_sex=incident["officerSex"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"],
            officer_identifier=incident["officerIdentifier"]
        )

        # TODO: re-evaluate what this return value means
        return True

#
# SANTA ROSA POLICE DEPARTMENT
#

class UseOfForceIncidentSRPD(SurrogatePK, Model):
    __tablename__ = 'use_of_force_incidents_srpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(128), unique=False, nullable=True)
    file_number = Column(db.String(128), unique=False, nullable=True)
    occurred_date = Column(db.DateTime, nullable=True)
    team = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    use_of_force_reason = Column(db.String(255), unique=False, nullable=True)
    aggravating_factors = Column(db.String(255), unique=False, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    resident_injured = Column(db.Boolean, nullable=True)
    resident_hospitalized = Column(db.Boolean, nullable=True)
    officer_injured = Column(db.Boolean, nullable=True)
    officer_hospitalized = Column(db.Boolean, nullable=True)
    officer_force_type = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("fileNumber", "file_number", "fileNumber"),
            ("occurredDate", "occurred_date", "occurredDate"),
            ("team", "team", "team"),
            ("assignment", "assignment", "assignment"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("serviceType", "service_type", "serviceType"),
            ("useOfForceReason", "use_of_force_reason", "useOfForceReason"),
            ("aggravatingFactors", "aggravating_factors", "aggravatingFactors"),
            ("arrestMade", "arrest_made", "arrestMade"),
            ("residentInjured", "resident_injured", "residentInjured"),
            ("residentHospitalized", "resident_hospitalized", "residentHospitalized"),
            ("officerInjured", "officer_injured", "officerInjured"),
            ("officerHospitalized", "officer_hospitalized", "officerHospitalized"),
            ("officerForceType", "officer_force_type", "officerForceType")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new UOF incident or update an existing one
        '''

        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the location
        incident["team"] = cleaner.capitalize(incident["team"])
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean force type
        incident["officerForceType"] = cleaner.officer_force_type(incident["officerForceType"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="uof")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            file_number=incident["fileNumber"],
            case_number=incident["caseNumber"],
            occurred_date=parse_date(incident["occurredDate"]),
            team=incident["team"],
            assignment=incident["assignment"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"],
            service_type=incident["serviceType"],
            use_of_force_reason=incident["useOfForceReason"],
            aggravating_factors=incident["aggravatingFactors"],
            arrest_made=incident["arrestMade"],
            resident_injured=incident["residentInjured"],
            resident_hospitalized=incident["residentHospitalized"],
            officer_injured=incident["officerInjured"],
            officer_hospitalized=incident["officerHospitalized"],
            officer_force_type=incident["officerForceType"]
        )

        # TODO: re-evaluate what this return value means
        return True

class CitizenComplaintSRPD(SurrogatePK, Model):
    __tablename__ = 'citizen_complaints_srpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(128), unique=False, nullable=True)
    file_number = Column(db.String(128), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    source = Column(db.String(255), unique=False, nullable=True)
    occurred_date = Column(db.DateTime, nullable=True)
    team = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    bureau = Column(db.String(255), unique=False, nullable=True)
    division = Column(db.String(255), unique=False, nullable=True)
    allegation = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("id", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("fileNumber", "file_number", "fileNumber"),
            ("serviceType", "service_type", "serviceType"),
            ("source", "source", "source"),
            ("occurredDate", "occurred_date", "occurredDate"),
            ("team", "team", "team"),
            ("assignment", "assignment", "assignment"),
            ("bureau", "bureau", "bureau"),
            ("division", "division", "division"),
            ("allegation", "allegation", "allegation"),
            ("disposition", "disposition", "disposition"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new Citizen Complaints incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize all the fields in the incident
        incident = cleaner.capitalize_incident(incident)
        # clean sex & race
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="complaints")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        # create the new incident row
        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            case_number=incident["caseNumber"],
            file_number=incident["fileNumber"],
            service_type=incident["serviceType"],
            source=incident["source"],
            occurred_date=parse_date(incident["occurredDate"]),
            team=incident["team"],
            assignment=incident["assignment"],
            bureau=incident["bureau"],
            division=incident["division"],
            allegation=incident["allegation"],
            disposition=incident["disposition"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"]
        )

        # TODO: re-evaluate what this return value means
        return True

class OfficerInvolvedShootingSRPD(SurrogatePK, Model):
    __tablename__ = 'officer_involved_shootings_srpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(128), unique=False, nullable=True)
    occurred_date = Column(db.DateTime, nullable=True)
    team = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    service_type = Column(db.String(255), unique=False, nullable=True)
    officer_weapon_used = Column(db.String(255), unique=False, nullable=True)
    intentional = Column(db.Boolean, nullable=True)
    resident_condition = Column(db.String(255), unique=False, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)
    disposition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''

        return [
            ("id", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("occurredDate", "occurred_date", "occurredDate"),
            ("team", "team", "team"),
            ("assignment", "assignment", "assignment"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("serviceType", "service_type", "serviceType"),
            ("officerWeaponUsed", "officer_weapon_used", "officerWeaponUsed"),
            ("intentional", "intentional", "intentional"),
            ("residentCondition", "resident_condition", "residentCondition"),
            ("officerCondition", "officer_condition", "officerCondition"),
            ("disposition", "disposition", "disposition")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new OIS incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the team and assignment
        incident["team"] = cleaner.capitalize(incident["team"])
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean weapon, race, gender
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="ois")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            case_number=incident["caseNumber"],
            occurred_date=parse_date(incident["occurredDate"]),
            team=incident["team"],
            assignment=incident["assignment"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            service_type=incident["serviceType"],
            officer_weapon_used=incident["officerWeaponUsed"],
            intentional=incident["intentional"],
            resident_condition=incident["residentCondition"],
            officer_condition=incident["officerCondition"],
            disposition=incident["disposition"]
        )

        # TODO: re-evaluate what this return value means
        return True

class PursuitSRPD(SurrogatePK, Model):
    __tablename__ = 'pursuits_srpd'
    department_id = Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    opaque_id = Column(db.String(255), unique=False, nullable=False)
    case_number = Column(db.String(128), unique=False, nullable=True)
    pursuit_number = Column(db.String(128), unique=False, nullable=True)
    occurred_date = Column(db.DateTime, nullable=True)
    team = Column(db.String(255), unique=False, nullable=True)
    assignment = Column(db.String(255), unique=False, nullable=True)
    officer_age = Column(db.String(255), unique=False, nullable=True)
    officer_years_of_service = Column(db.String(255), unique=False, nullable=True)
    aborted = Column(db.Boolean, nullable=True)
    accident = Column(db.Boolean, nullable=True)
    arrest_made = Column(db.Boolean, nullable=True)
    distance = Column(db.String(255), unique=False, nullable=True)
    reason = Column(db.String(255), unique=False, nullable=True)
    vehicle_type = Column(db.String(255), unique=False, nullable=True)
    max_speed = Column(db.String(255), unique=False, nullable=True)
    resident_race = Column(db.String(255), unique=False, nullable=True)
    resident_sex = Column(db.String(255), unique=False, nullable=True)
    resident_age = Column(db.String(255), unique=False, nullable=True)
    copter_available = Column(db.Boolean, nullable=True)
    copter_used = Column(db.Boolean, nullable=True)
    dui_arrest = Column(db.Boolean, nullable=True)
    stop_device_used = Column(db.Boolean, nullable=True)
    stop_device = Column(db.String(255), unique=False, nullable=True)
    follow_policy = Column(db.Boolean, nullable=True)
    weather_condition = Column(db.String(255), unique=False, nullable=True)
    location_began = Column(db.String(255), unique=False, nullable=True)
    location_ended = Column(db.String(255), unique=False, nullable=True)
    in_car_cam_available = Column(db.Boolean, nullable=True)
    in_car_cam_used = Column(db.Boolean, nullable=True)
    total_time_minutes = Column(db.String(255), unique=False, nullable=True)
    influencing_factor = Column(db.String(255), unique=False, nullable=True)
    aborted_by = Column(db.String(255), unique=False, nullable=True)
    concluded_by = Column(db.String(255), unique=False, nullable=True)
    damage_type = Column(db.String(255), unique=False, nullable=True)
    injury_type = Column(db.String(255), unique=False, nullable=True)
    initiated_by_agency = Column(db.String(255), unique=False, nullable=True)
    concluded_by_agency = Column(db.String(255), unique=False, nullable=True)
    liability_claim = Column(db.Boolean, nullable=True)
    associated_officer_count = Column(db.String(255), unique=False, nullable=True)
    violation = Column(db.String(255), unique=False, nullable=True)
    justified = Column(db.Boolean, nullable=True)
    officer_condition = Column(db.String(255), unique=False, nullable=True)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    @classmethod
    def get_csv_schema(cls):
        ''' Return the CSV column headers and variable names, along with the variable names expected from the extractor.
        '''
        return [
            ("opaqueId", "opaque_id", "opaqueId"),
            ("caseNumber", "case_number", "caseNumber"),
            ("pursuitNumber", "pursuit_number", "pursuitNumber"),
            ("occurredDate", "occurred_date", "occurredDate"),
            ("team", "team", "team"),
            ("assignment", "assignment", "assignment"),
            ("officerAge", "officer_age", "officerAge"),
            ("officerYearsOfService", "officer_years_of_service", "officerYearsOfService"),
            ("aborted", "aborted", "aborted"),
            ("accident", "accident", "accident"),
            ("arrestMade", "arrest_made", "arrestMade"),
            ("distance", "distance", "distance"),
            ("reason", "reason", "reason"),
            ("vehicleType", "vehicle_type", "vehicleType"),
            ("maxSpeed", "max_speed", "maxSpeed"),
            ("residentRace", "resident_race", "residentRace"),
            ("residentSex", "resident_sex", "residentSex"),
            ("residentAge", "resident_age", "residentAge"),
            ("copterAvailable", "copter_available", "copterAvailable"),
            ("copterUsed", "copter_used", "copterUsed"),
            ("duiArrest", "dui_arrest", "duiArrest"),
            ("stopDeviceUsed", "stop_device_used", "stopDeviceUsed"),
            ("stopDevice", "stop_device", "stopDevice"),
            ("followPolicy", "follow_policy", "followPolicy"),
            ("weatherCondition", "weather_condition", "weatherCondition"),
            ("locationBegan", "location_began", "locationBegan"),
            ("locationEnded", "location_ended", "locationEnded"),
            ("inCarCamAvailable", "in_car_cam_available", "inCarCamAvailable"),
            ("inCarCamUsed", "in_car_cam_used", "inCarCamUsed"),
            ("totalTimeMinutes", "total_time_minutes", "totalTimeMinutes"),
            ("influencingFactor", "influencing_factor", "influencingFactor"),
            ("abortedBy", "aborted_by", "abortedBy"),
            ("concludedBy", "concluded_by", "concludedBy"),
            ("damageType", "damage_type", "damageType"),
            ("injuryType", "injury_type", "injuryType"),
            ("initiatedByAgency", "initiated_by_agency", "initiatedByAgency"),
            ("concludedByAgency", "concluded_by_agency", "concludedByAgency"),
            ("liabilityClaim", "liability_claim", "liabilityClaim"),
            ("associatedOfficerCount", "associated_officer_count", "associatedOfficerCount"),
            ("violation", "violation", "violation"),
            ("justified", "justified", "justified"),
            ("officerCondition", "officer_condition", "officerCondition")
        ]

    @classmethod
    def add_or_update_incident(cls, department, incident):
        ''' Add a new pursuit incident or update an existing one
        '''
        # get a cleaner instance
        cleaner = Cleaners()
        # capitalize the team and assignment
        incident["team"] = cleaner.capitalize(incident["team"])
        incident["assignment"] = cleaner.capitalize(incident["assignment"])
        # clean race, gender
        incident["residentSex"] = cleaner.sex(incident["residentSex"])
        incident["residentRace"] = cleaner.race(incident["residentRace"])
        # capitalize others
        incident["distance"] = cleaner.capitalize(incident["distance"])
        incident["reason"] = cleaner.capitalize(incident["reason"])
        incident["vehicleType"] = cleaner.capitalize(incident["vehicleType"])
        incident["stopDevice"] = cleaner.capitalize(incident["stopDevice"])
        incident["weatherCondition"] = cleaner.capitalize(incident["weatherCondition"])
        incident["locationBegan"] = cleaner.capitalize(incident["locationBegan"])
        incident["locationEnded"] = cleaner.capitalize(incident["locationEnded"])
        incident["influencingFactor"] = cleaner.capitalize(incident["influencingFactor"])
        incident["violation"] = cleaner.capitalize(incident["violation"])
        incident["abortedBy"] = cleaner.capitalize(incident["abortedBy"])
        incident["concludedBy"] = cleaner.capitalize(incident["concludedBy"])
        incident["damageType"] = cleaner.capitalize(incident["damageType"])
        incident["injuryType"] = cleaner.capitalize(incident["injuryType"])
        incident["initiatedByAgency"] = cleaner.capitalize(incident["initiatedByAgency"])
        incident["concludedByAgency"] = cleaner.capitalize(incident["concludedByAgency"])
        incident["officerCondition"] = cleaner.capitalize(incident["officerCondition"])

        # check and set the incident last updated
        incident_kwargs = dict(opaque_id=incident["opaqueId"], department_id=department.id, incident_type="pursuits")
        incident_updated = IncidentsUpdated.query.filter_by(**incident_kwargs).first()
        # this is the first time we've encountered this incident in this update
        if not incident_updated:
            # delete this incident's rows from the database
            cls.query.filter_by(opaque_id=incident["opaqueId"]).delete()
            db.session.commit()
            # remember it for this incident's following rows in this update
            IncidentsUpdated.create(**incident_kwargs)

        cls.create(
            department_id=department.id,
            opaque_id=incident["opaqueId"],
            case_number=incident["caseNumber"],
            pursuit_number=incident["pursuitNumber"],
            occurred_date=incident["occurredDate"],
            team=incident["team"],
            assignment=incident["assignment"],
            officer_age=incident["officerAge"],
            officer_years_of_service=incident["officerYearsOfService"],
            aborted=incident["aborted"],
            accident=incident["accident"],
            arrest_made=incident["arrestMade"],
            distance=incident["distance"],
            reason=incident["reason"],
            vehicle_type=incident["vehicleType"],
            max_speed=incident["maxSpeed"],
            resident_race=incident["residentRace"],
            resident_sex=incident["residentSex"],
            resident_age=incident["residentAge"],
            copter_available=incident["copterAvailable"],
            copter_used=incident["copterUsed"],
            dui_arrest=incident["duiArrest"],
            stop_device_used=incident["stopDeviceUsed"],
            stop_device=incident["stopDevice"],
            follow_policy=incident["followPolicy"],
            weather_condition=incident["weatherCondition"],
            location_began=incident["locationBegan"],
            location_ended=incident["locationEnded"],
            in_car_cam_available=incident["inCarCamAvailable"],
            in_car_cam_used=incident["inCarCamUsed"],
            total_time_minutes=incident["totalTimeMinutes"],
            influencing_factor=incident["influencingFactor"],
            aborted_by=incident["abortedBy"],
            concluded_by=incident["concludedBy"],
            damage_type=incident["damageType"],
            injury_type=incident["injuryType"],
            initiated_by_agency=incident["initiatedByAgency"],
            concluded_by_agency=incident["concludedByAgency"],
            liability_claim=incident["liabilityClaim"],
            associated_officer_count=incident["associatedOfficerCount"],
            violation=incident["violation"],
            justified=incident["justified"],
            officer_condition=incident["officerCondition"]
        )

        # TODO: re-evaluate what this return value means
        return True
