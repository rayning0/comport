# -*- coding: utf-8 -*-
import datetime as dt
from comport.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)
from comport.content.models import ChartBlockDefaults

from flask import current_app
from comport.utils import coalesce_date
from comport.user.models import User, Role
from .defaults import DepartmentDefaults
import csv
import io

class Department(SurrogatePK, Model):
    __tablename__ = 'departments'
    id = Column(db.Integer, primary_key=True, index=True)
    name = Column(db.String(80), unique=True, nullable=False)
    invite_codes = relationship("Invite_Code", backref="department")
    users = relationship("User", backref="department")
    use_of_force_incidents = relationship("UseOfForceIncident", backref="department")
    citizen_complaints = relationship("CitizenComplaint", backref="department")
    officer_involved_shootings = relationship("OfficerInvolvedShooting", backref="department")
    chart_blocks = relationship("ChartBlock", backref="department")
    denominator_values = relationship("DenominatorValue", backref="department")
    why_we_are_doing_this = Column(db.Text( convert_unicode=True), unique=False, nullable=True)
    how_you_can_use_this_data = Column(db.Text( convert_unicode=True), unique=False, nullable=True)
    contact_us = Column(db.Text( convert_unicode=True), unique=False, nullable=True)
    links = relationship("Link", backref="department")

    def get_links_by_type(self,type):
        return list(filter(lambda l: l.type == type, self.links))

    def get_uof_blocks(self):
        return dict([(block.slug, block) for block in self.chart_blocks if block.dataset == "Use of Force"])

    def get_complaint_blocks(self):
        return dict([(block.slug, block) for block in self.chart_blocks if block.dataset == "complaints"])

    def get_extractor(self):
        extractors = list(filter(lambda u: u.type == "extractors" ,self.users))
        return extractors[0] if extractors else None

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)
        self.what_this_is = DepartmentDefaults.what_this_is
        self.why_we_are_doing_this = DepartmentDefaults.why_we_are_doing_this
        self.how_you_can_use_this_data = DepartmentDefaults.how_you_can_use_this_data
        self.contact_us = DepartmentDefaults.contact_us

        for default_chart_block in ChartBlockDefaults.query.all():
            self.chart_blocks.append(default_chart_block.make_real_block())

    def __repr__(self):
        return '<Department({name})>'.format(name=self.name)

    def get_uof_csv(self):
        csv = "id,occuredDate,division,precinct,shift,beat,disposition,censusTract,officerForceType,residentResistType,officerWeaponUsed,residentWeaponUsed,serviceType,arrestMade,arrestCharges,residentInjured,residentHospitalized,officerInjured,officerHospitalized,residentCondition,officerCondition,useOfForceReason,residentRace,officerRace,residentAge,officerAge,officerYearsOfService,officerIdentifier\n"
        use_of_force_incidents = self.use_of_force_incidents
        for incident in use_of_force_incidents:
            csv += incident.to_csv_row()
        return csv


    def get_complaint_csv(self):
        output = io.StringIO()

        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(["id","occuredDate","division","precinct","shift","beat","disposition","allegationType","allegation","censusTract","residentRace","residentSex","residentAge","officerRace","officerSex","officerAge","officerYearsOfService","officerIdentifier"])

        complaints = self.citizen_complaints

        for complaint in complaints:
            occured_date = coalesce_date(complaint.occured_date)
            values = [
                complaint.opaque_id,
                occured_date,
                complaint.division,
                complaint.precinct,
                complaint.shift,
                complaint.beat,
                complaint.disposition,
                complaint.allegation_type,
                complaint.allegation,
                complaint.census_tract,
                complaint.resident_race,
                complaint.resident_sex,
                complaint.resident_age,
                complaint.officer_race,
                complaint.officer_sex,
                complaint.officer_age,
                complaint.officer_years_of_service,
                complaint.officer_identifier
            ]
            writer.writerow(values)

        return output.getvalue()


    def get_ois_csv(self):
        csv = "id,occuredDate,division,precinct,shift,beat,disposition,censusTract,officerForceType,residentWeaponUsed,serviceType,residentRace,officerRace,residentSex,officerSex,officerIdentifier,officerYearsOfService,officerAge,residentAge,officerCondition,residentCondition\n"
        officer_involved_shootings = self.officer_involved_shooting
        for incident in officer_involved_shootings:
            csv += incident.to_csv_row()
        return csv

    def get_denominator_csv(self):
        csv = "month,year,arrests,callsForService,officerInitiatedCalls\n"
        denominator_values = self.denominator_values
        for month in denominator_values:
            csv += month.to_csv_row()
        return csv

class Extractor(User):
    __tablename__ = 'extractors'
    id = Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    next_month = Column(db.Integer)
    next_year = Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':'extractors',
        'inherit_condition': (id==User.id)
    }

    def generate_envs(self, password):
        return """
            COMPORT_BASE_URL="%s"
            COMPORT_USERNAME="%s"
            COMPORT_PASSWORD="%s"
            COMPORT_DEPARTMENT_ID="%s"
            COMPORT_SQL_SERVER_URL =
            COMPORT_SQL_SERVER_DATABASE =
            COMPORT_SQL_SERVER_USERNAME =
            COMPORT_SQL_SERVER_PASSWORD =
        """ % (current_app.config["BASE_URL"], self.username, password, self.department_id,)

    def from_department_and_password(department, password):
        extractor = Extractor.create(username='%s-extractor' % department.name.replace (" ", "_"), email='extractor@example.com', department_id=department.id, password=password)
        extractor.roles.append(Role.create(name="extractor"))
        extractor.save()

        envs = extractor.generate_envs(password)

        return (extractor,envs)
