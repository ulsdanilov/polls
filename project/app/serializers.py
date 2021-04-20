from rest_framework import serializers

from project.app.models import Choice, Poll, Question, UserAnswer, UserForm


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['pk', 'question', 'title']


class QuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.ChoiceField(choices=Question.QuestionType.choices, default=Question.QuestionType.SINGLE)
    question_choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['pk', 'poll', 'text', 'question_type', 'question_choices']


class PollSerializer(serializers.ModelSerializer):
    poll_questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['pk', 'title', 'description', 'start_date', 'end_date', 'poll_questions']

    def update(self, instance, validated_data):
        if 'start_date' in validated_data:
            raise serializers.ValidationError({'start_date': 'Нельзя изменить поле'})

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ['pk', 'question', 'choices', 'custom_answer']

    def validate(self, attrs):
        if attrs['question'].question_type == 'SINGLE' and len(attrs['choices']) != 1:  # pylint: disable=no-else-raise
            raise serializers.ValidationError({attrs['question'].text: 'Выберите один вариант ответа'})

        elif attrs['question'].question_type == 'MULTIPLE' and len(attrs['choices']) <= 1:
            raise serializers.ValidationError({attrs['question'].text: 'Выберите несколько вариантов ответа'})

        elif attrs['question'].question_type == 'CUSTOM' and len(attrs['custom_answer']) == 0:
            raise serializers.ValidationError({attrs['question'].text: 'Введите свой вариант ответа'})

        else:
            return attrs

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        user_answer = UserAnswer.objects.create(**validated_data)
        user_answer.choices.set(choices)
        user_answer.save()

        return user_answer

    def update(self, instance, validated_data):
        if 'choices' in validated_data:
            choices = validated_data.pop('choices')
            instance.choices.set(choices)

        return super(UserAnswerSerializer, self).update(instance, validated_data)


class UserFormSerializer(serializers.ModelSerializer):
    phone_number = serializers.RegexField(regex=r'^\d{1,11}$', required=False)
    user_answers = UserAnswerSerializer(many=True)

    class Meta:
        model = UserForm
        extra_kwargs = {
            'user': {'read_only': True},
            'create_datetime': {'read_only': True},
        }
        fields = ['pk', 'poll', 'phone_number', 'email', 'create_datetime', 'user_answers']

    def create(self, validated_data):
        user_form = UserForm.objects.filter(
            user=validated_data['user'],
            poll=validated_data['poll']
        )
        if user_form:
            raise serializers.ValidationError({'poll_id': 'Опрос уже пройден'})

        answers = validated_data.pop('user_answers')
        user_form = UserForm.objects.create(**validated_data)

        for answer in answers:
            user_answer = UserAnswer.objects.create(
                user_form=user_form,
                question=answer['question'],
                custom_answer=answer['custom_answer'] if answer['question'].question_type == 'CUSTOM' else None
            )
            user_answer.choices.set(answer['choices'])
            user_answer.save()

        return user_form
