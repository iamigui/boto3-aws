import boto3
from colorama import init, Fore, Back, Style
import sys

#Falta añadir colores

init(autoreset=True)

def checkUser():
    try:
        print('Insert the name of the user: ')
        iam = boto3.client('iam')
        username = input()
        username_encontrada = False
        paginator = iam.get_paginator('list_users')

        for response in paginator.paginate():
            for user in response['Users']:
                if username == user['UserName']:
                    arn = user['Arn']
                    print(Fore.GREEN + '\nThe username: ' + username + ' exists.')
                    username_encontrada = True
                    break

        if not username_encontrada:
            print(Fore.RED + '\nUnknown user.')
            sys.exit(1)
    
    except Exception as e:
        print(Fore.RED +'An error occurred:', e)

def listPolicies():
        try:
            iam = boto3.client('iam')
            policy_encontrada = False
            paginator = iam.get_paginator('list_policies')
            print('I need to know the ARN from the policy you look for...')
            print('Select how you want to display the policies:\n')
            print('1) Verify the policy ARN: ')
            print('2) List all policies: ')
            print('3) Check the policies that contain the text: \n')

            respuesta = input()
            
            if respuesta == '1':
                print('Tell me the name of policy: ')
                global policy_name
                policy_name = input(str())
                for response in paginator.paginate(Scope='All'):
                    for policy in response['Policies']:
                        if policy_name == policy['PolicyName']:
                            Arn = policy['Arn']
                            print('Policy Name : {} Arn : {}'.format(policy_name, Arn))
                            policy_encontrada = True
                            break

                if not policy_encontrada:
                    print('Unknown policy name.\n')

            elif respuesta == '2' :
                print('This is the list of policies from AWS:')
                for response in paginator.paginate(Scope="AWS"): #The scope can be changed to the customer, Local or AWS to list all policies
                    for policy in response['Policies']:
                        policy_name = policy['PolicyName']
                        Arn = policy['Arn']

                        print('Policy Name : {} Arn : {}'.format(policy_name, Arn))

            elif respuesta == '3':
                print('Tell me the name of policy: ')
                policy_name = input(str())
                for response in paginator.paginate(Scope='All'):
                    for policy in response['Policies']:
                        if policy_name in policy['PolicyName']:
                            Arn = policy['Arn']
                            print('Policy Name : {} Arn : {}'.format(policy['PolicyName'], Arn))
                            policy_encontrada = True
                            break

                if not policy_encontrada:
                    print(Fore.RED +'Unknown policy name.')

            else:
                print(Fore.RED +'\nNot valid option.')

        except Exception as e:
            print(Fore.RED +'An error occurred:', e)
            sys.exit(1)

def attachPolicy(policy_arn, username):
    try:
        iam = boto3.client('iam')

        response = iam.attach_user_policy(
            UserName = username,
            PolicyArn = policy_arn
        )

        print(Fore.GREEN + 'The policy ' + policy_name + ' has been attached to the user: ' + username)
    
    except Exception as e:
        print(Fore.RED +'An error occurred:', e)
        sys.exit(1)

def detachPolicy(arn, username):
    try:
        iam = boto3.client('iam')

        response = iam.detack_user_policy(
            UserName = username,
            PolicyArn = policy_arn
        )

        print(Fore.GREEN + 'The policy ' + policy_name + ' has been detached from the user: ' + username)
    
    except Exception as e:
        print(Fore.RED +'An error occurred:', e)
        sys.exit(1)

if __name__ == "__main__":
    print('This is a function to attach policies to users.\n')
    checkUser()

    listPolicies()

    print('Insert the policy ARN: ')
    policy_arn = input()

    attachPolicy(policy_arn, username)