from django.db import models

class Team(models.Model):
    teamId = models.AutoField(primary_key=True),
    teamName = models.CharField(max_length=255),
    league = models.CharField(max_length=255),
    accumulatedPoint = models.IntegerField(),
    affiliation = models.CharField(max_length=255),
    lateSubmissionDateTime = models.DateTimeField(),
    currentPhase = models.CharField(max_length=255)

    def __str__(self):
        return self.teamName
    

class Participant(models.Model):
    participantId = models.AutoField(primary_key=True),
    team = models.ForeignKey(Team, on_delete=models.CASCADE),
    email = models.CharField(max_length=255),
    userName = models.CharField(max_length=255),
    firstName = models.CharField(max_length=255),
    lastName = models.CharField(max_length=255),
    gender = models.CharField(max_length=255),
    course = models.CharField(max_length=255),
    cohort = models.CharField(max_length=255),
    dateJoined = models.DateTimeField(),
    role = models.CharField(max_length=255),
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    

class Phase(models.Model):
    phaseId = models.AutoField(primary_key=True),
    phaseName = models.CharField(max_length=255),
    startDate = models.DateTimeField(),
    endDate = models.DateField(),
    status = models.CharField(max_length=25)

    def __str__(self):
        return self.phaseName
    

class Submission(models.Model):
    submissionId =  models.AutoField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    phase = models.ForeignKey()
    SubmissionDateTime = models.DateTimeField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"Submission {self.submissionID} by {self.team.teamName}"


class Score(models.Model):
    scoreId = models.AutoField(primary_key=True),
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    criteriaId = models.IntegerField()
    assignedPoints = models.IntegerField()

    def __str__(self):
        return f"Score {self.scoreID} for Submission {self.submissionID}"
    

class judgingCriteria(models.Model):
    criteriaId = models.AutoField(primary_key=True)
    criterionName = models.CharField(max_length=255)
    maxPoints = models.IntegerField()

    def __str__(self):
        return self.criterionName