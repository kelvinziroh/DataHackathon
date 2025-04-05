from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    accumulatedPoint = models.IntegerField()
    affiliation = models.CharField(max_length=255)
    lateSubmissionDateTime = models.DateTimeField()
    currentPhase = models.CharField(max_length=255)

    def __str__(self):
        return self.teamName

class Participant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    participantId = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    cohort = models.CharField(max_length=255, null=True, blank=True)  # Optional to avoid future issues
    dateJoined = models.DateTimeField()
    role = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    confidenceScore = models.IntegerField()

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Phase(models.Model):
    phaseId = models.AutoField(primary_key=True)
    phaseName = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateField()
    status = models.CharField(max_length=25)

    def __str__(self):
        return self.phaseName

class Submission(models.Model):
    submissionId = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    SubmissionDateTime = models.DateTimeField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"Submission {self.submissionId} by {self.team.teamName}"

class Score(models.Model):
    scoreId = models.AutoField(primary_key=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    criteriaId = models.IntegerField()
    assignedPoints = models.IntegerField()

    def __str__(self):
        return f"Score {self.scoreId} for Submission {self.submission.submissionId}"

class JudgingCriteria(models.Model):
    criteriaId = models.AutoField(primary_key=True)
    criterionName = models.CharField(max_length=255)
    maxPoints = models.IntegerField()

    def __str__(self):
        return self.criterionName
