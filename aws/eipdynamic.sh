#!/bin/sh
# get ec2 instance id by tag
InstanceId=$(aws ec2 describe-instances --filters "Name=instance-type,Values=c5.xlarge" "Name=instance-state-name,Values=running"  --query "Reservations[*].Instances[*].[InstanceId]" --output text)
OldPublicIpAddress=$(aws ec2 describe-instances --filters "Name=instance-type,Values=c5.xlarge" "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].[PublicIpAddress]" --output text)

#for i in $( seq 1 20)
#do
#	aws ec2 allocate-address --domain vpc --query "PublicIp" --output text
#done
# disassociate&release address
for x in $OldPublicIpAddress
do
	if [ $x != "None" ]
	then 
		#echo $x
		aws ec2 disassociate-address --public-ip $x
		aws ec2 release-address --allocation-id $(aws ec2 describe-addresses --filters "Name=public-ip,Values=$x" --query "Addresses[*].[AllocationId]" --output text)
	fi
done

# generate an elastic ip address
#NewPublicIpAddress=$(aws ec2 allocate-address --domain vpc --query "PublicIp" --output text)
# associate an elastic ip to an existed ec2 instance
:'
for x in $InstanceId
do
	pIp=$(aws ec2 allocate-address --domain vpc --query "PublicIp" --output text)
	result=$(aws ec2 associate-address --instance-id $x --public-ip  $pIp )
	echo $pIp
	#echo "New Elastic IP: "$result
done
'
# release an existed elastic ip address
#aws ec2 release-address --allocation-id $(aws ec2 describe-addresses --filters "Name=public-ip,Values=$OldPublicIpAddress" --query "Addresses[*].[AllocationId]" --output text)

